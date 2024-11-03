# backtest_framework/backtest/backtest_runner.py

from backtesting import Backtest 
import logging
from multiprocessing import Pool, cpu_count
import pandas as pd  # Import pandas for type checking

# Do not configure logging here; it's configured in main.py
logger = logging.getLogger(__name__)

class BacktestRunner:
    def __init__(self, strategies, data_dict, transaction_costs=0.001, slippage=0.0005):
        """
        Initialize the BacktestRunner.

        Parameters:
            strategies (list): List of strategy classes to backtest.
            data_dict (dict): Dictionary containing processed data for each asset and timeframe.
            transaction_costs (float): Transaction cost per trade (default 0.1%).
            slippage (float): Slippage percentage (default 0.05%).
        """
        self.strategies = strategies
        self.data_dict = data_dict
        self.transaction_costs = transaction_costs
        self.slippage = slippage
        self.results = {}
    def run_backtests(self, concurrent=False):
        """
        Execute backtests for all strategies and assets.

        Parameters:
            concurrent (bool): Whether to run backtests concurrently. Default is False.
        """
        if concurrent:
            self._run_backtests_concurrently()
        else:
            self._run_backtests_sequentially()
    
    def _run_backtests_sequentially(self):
        """
        Run backtests sequentially.
        """
        for strategy_class in self.strategies:
            for asset, timeframes in self.data_dict.items():
                key, output = self._run_single_backtest(strategy_class, asset, timeframes)
                if output is not None:
                    self.results[key] = output

    def _run_backtests_concurrently(self):
        """
        Run backtests concurrently using multiprocessing.
        """
        tasks = []
        for strategy_class in self.strategies:
            for asset, timeframes in self.data_dict.items():
                tasks.append((strategy_class, asset, timeframes))

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(self._run_single_backtest, tasks)
            for key, output in results:
                if output is not None:
                    self.results[key] = output

    def run_single_backtest(self, strategy_class, asset, timeframes, **strategy_params):
        """
        Run a single backtest for a given strategy and asset.

        Parameters:
            strategy_class (class): The strategy class to backtest.
            asset (str): The asset symbol (e.g., 'BTCUSD').
            timeframes (dict): Dictionary of timeframes and their corresponding data.
            strategy_params (dict): Dictionary of parameters to pass to the strategy.

        Returns:
            tuple: (strategy_asset_key, backtest_result)
        """
        key = f"{strategy_class.__name__}_{asset}"
        logger.info(f"Starting backtest for Strategy: {strategy_class.__name__}, Asset: {asset}")

        try:
            # Retrieve the strategy's primary_tf
            primary_tf = getattr(strategy_class, 'primary_tf', '1m')
            logger.info(f"Strategy {strategy_class.__name__} has primary_tf={primary_tf}")

            # Check if primary_tf data is available
            if primary_tf not in timeframes:
                logger.error(f"Primary timeframe '{primary_tf}' not found for asset '{asset}'. Skipping backtest.")
                return (key, None)

            # Retrieve and verify data
            data = timeframes[primary_tf]
            if not isinstance(data, pd.DataFrame):
                logger.error(f"Data for {asset} at {primary_tf} is not a pandas DataFrame. It's a {type(data)}. Skipping backtest.")
                return (key, None)

            # Check if 'Close' column exists
            if 'Close' not in data.columns:
                logger.error(f"'Close' column missing in data for {asset} at {primary_tf} timeframe. Skipping backtest.")
                return (key, None)

            # Log the first few rows of the data
            logger.info(f"Data for {asset} at {primary_tf} timeframe:\n{data.head()}")

            # Prepare additional timeframes if required
            additional_strategy_kwargs = {}
            if getattr(strategy_class, 'requires_multiple_timeframes', False):
                # Identify additional required timeframes
                higher_tf = getattr(strategy_class, 'higher_tf', None)
                if higher_tf:
                    if higher_tf not in timeframes:
                        logger.error(f"Higher timeframe '{higher_tf}' not found for asset '{asset}'. Skipping backtest.")
                        return (key, None)
                    higher_data = timeframes[higher_tf]
                    if not isinstance(higher_data, pd.DataFrame):
                        logger.error(f"Data for {asset} at {higher_tf} is not a pandas DataFrame. It's a {type(higher_data)}. Skipping backtest.")
                        return (key, None)
                    if 'Close' not in higher_data.columns:
                        logger.error(f"'Close' column missing in data for {asset} at {higher_tf} timeframe. Skipping backtest.")
                        return (key, None)
                    # Pass 'higher_tf_data' as the key
                    additional_strategy_kwargs['higher_tf_data'] = higher_data
                    logger.info(f"Passing higher_tf data '{higher_tf}' to {strategy_class.__name__}")

            # Merge strategy_params and additional_strategy_kwargs
            total_strategy_params = {**strategy_params, **additional_strategy_kwargs}

            # Initialize Backtest with the strategy's primary_tf data
            bt = Backtest(
                data=data,
                strategy=strategy_class,
                cash=100000,  # Starting with $100,000
                commission=self.transaction_costs,
                exclusive_orders=False if getattr(strategy_class, 'requires_multiple_timeframes', False) else True
            )

            # Log strategy_kwargs
            logger.info(f"strategy_kwargs for {key}: {total_strategy_params}")

            # Run the backtest with strategy-specific parameters
            output = bt.run(**total_strategy_params)

            logger.info(f"Completed backtest for {key}")
            return (key, output)

        except Exception as e:
            logger.error(f"Error running backtest for Strategy: {strategy_class.__name__}, Asset: {asset}. Error: {e}")
            return (key, None)


    def get_results(self):
        """
        Retrieve the backtest results.

        Returns:
            dict: Dictionary containing backtest results.
        """
        return self.results

    def optimize(self, strategy_class, data, param_ranges, metric, maximize=True, constraint=None, max_cores=1, strategy_kwargs=None):
        logger.info(f"Starting optimization for strategy {strategy_class.__name__} using backtesting.py's optimize()")

        # Initialize Backtest without passing strategy_kwargs
        bt = Backtest(
            data,
            strategy_class,
            cash=100000,
            commission=self.transaction_costs,
            exclusive_orders=True
        )

        # Run optimize() and pass strategy_kwargs here
        stats, heatmap = bt.optimize(
            **param_ranges,
            maximize=metric if maximize else None,
            minimize=None if maximize else metric,
            constraint=constraint,
            max_cores=max_cores,
            return_heatmap=True,
            **(strategy_kwargs or {})
        )

        logger.info(f"Optimization completed for strategy {strategy_class.__name__}")

        return stats, heatmap