# optimization/random_search_optimizer.py

import logging
import pandas as pd
import random
from joblib import Parallel, delayed
from backtesting import Backtest

class RandomSearchOptimizer:
    def __init__(self, backtest_runner, strategy_class, data, data_dict, logger=None):
        self.backtest_runner = backtest_runner
        self.strategy_class = strategy_class
        self.data = data
        self.data_dict = data_dict  # To access higher timeframe data
        self.logger = logger or logging.getLogger(__name__)
        # Prepare higher_tf_data once
        self.higher_tf_data = self._prepare_higher_tf_data()

    def optimize(self, param_distributions, n_iter, metric, maximize=True, constraint=None, max_cores=-1):
        """
        Perform random search optimization using joblib for parallel execution.

        Parameters:
            param_distributions (dict): Parameter distributions for random sampling.
            n_iter (int): Number of iterations (random samples).
            metric (str): Performance metric to optimize.
            maximize (bool): Whether to maximize or minimize the metric.
            constraint (function): A function that imposes constraints on parameters.
            max_cores (int): Number of CPU cores to use (-1 uses all cores).

        Returns:
            best_result (pd.Series): The best parameters and their corresponding metrics.
            df_results (pd.DataFrame): DataFrame of results.
        """
        self.logger.info(f"Starting Random Search Optimization with joblib")

        param_names = list(param_distributions.keys())
        sampled_params = []
        sampled_params_set = set()

        # Sample random parameter combinations
        while len(sampled_params) < n_iter:
            params = {key: random.choice(values) for key, values in param_distributions.items()}
            if constraint and not constraint(params):
                continue
            param_tuple = tuple(params[key] for key in param_names)
            if param_tuple not in sampled_params_set:
                sampled_params.append(params)
                sampled_params_set.add(param_tuple)

        self.logger.info(f"Total sampled parameter combinations: {len(sampled_params)}")

        # Run backtests in parallel using joblib
        results = Parallel(n_jobs=max_cores)(
            delayed(self._run_backtest)(params)
            for params in sampled_params
        )

        # Collect and process results
        results = [res for res in results if res is not None]
        df_results = pd.DataFrame(results)

        # Find best parameters
        if maximize:
            best_result = df_results.loc[df_results[metric].idxmax()]
        else:
            best_result = df_results.loc[df_results[metric].idxmin()]

        self.logger.info("Random Search Optimization Completed with joblib")
        return best_result, df_results

    def _run_backtest(self, param_dict):
        """
        Run a single backtest with the given parameters.

        Parameters:
            param_dict (dict): Dictionary of parameters for the strategy.

        Returns:
            dict: Result containing parameters and performance metrics.
        """
        try:
            # Deep copy the strategy class to avoid interference between processes
            import copy
            strategy_class = copy.deepcopy(self.strategy_class)

            # Update strategy parameters
            for key, value in param_dict.items():
                setattr(strategy_class, key, value)

            # Prepare strategy_kwargs with higher_tf_data
            strategy_kwargs = {'higher_tf_data': self.higher_tf_data} if self.higher_tf_data is not None else {}

            # Initialize Backtest
            bt = Backtest(
                data=self.data,
                strategy=strategy_class,
                cash=100000,
                commission=self.backtest_runner.transaction_costs,
                exclusive_orders=True
            )

            # Run backtest
            output = bt.run(**strategy_kwargs)

            # Get the metric
            metric_value = output[param_dict.get('metric', 'Equity Final [$]')]
            record = param_dict.copy()
            record[param_dict.get('metric', 'Equity Final [$]')] = metric_value

            # Store other metrics as needed
            for m in ['Equity Final [$]', 'Sharpe Ratio', 'Calmar Ratio', 'Win Rate [%]', 'Max Drawdown [%]']:
                record[m] = output.get(m, None)

            return record

        except Exception as e:
            self.logger.error(f"Error running backtest with params {param_dict}: {e}")
            return None

    def _prepare_higher_tf_data(self):
        """
        Prepare higher_tf_data to pass to the strategy.

        Returns:
            higher_tf_data (pd.DataFrame): Higher timeframe data.
        """
        if getattr(self.strategy_class, 'requires_multiple_timeframes', False):
            higher_tf = getattr(self.strategy_class, 'higher_tf', None)
            if higher_tf:
                higher_tf_data = self.data_dict.get(higher_tf)
                if higher_tf_data is None:
                    self.logger.error(f"Higher timeframe data '{higher_tf}' not found.")
                    raise ValueError(f"Higher timeframe data '{higher_tf}' not found.")
                return higher_tf_data
        return None
