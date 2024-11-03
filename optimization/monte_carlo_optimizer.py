# optimization/monte_carlo_optimizer.py

import logging
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import os

class MonteCarloOptimizer:
    def __init__(self, backtest_runner, strategy_class, asset, data, data_dict, logger=None):
        """
        Initialize the MonteCarloOptimizer.

        Parameters:
            backtest_runner (BacktestRunner): Instance of BacktestRunner.
            strategy_class (class): The strategy class to optimize.
            asset (str): The asset symbol (e.g., 'BTCUSD').
            data (pd.DataFrame): DataFrame of the primary timeframe data.
            data_dict (dict): Dictionary containing all data for the asset, including higher timeframes.
            logger (logging.Logger, optional): Logger instance.
        """
        self.backtest_runner = backtest_runner
        self.strategy_class = strategy_class
        self.asset = asset
        self.data = data
        self.data_dict = data_dict
        self.logger = logger or logging.getLogger(__name__)

    def _simulate(self, seed, param_ranges, perturb_data):
        """
        Perform a single Monte Carlo simulation.

        Parameters:
            seed (int): Random seed for reproducibility.
            param_ranges (dict): Dictionary of parameter ranges (low, high) for each parameter.
            perturb_data (bool): Whether to perturb the data.

        Returns:
            dict: Dictionary containing parameters and performance.
        """
        np.random.seed(seed)
        # Randomly select parameters within the specified ranges
        params = {}
        for param, (low, high) in param_ranges.items():
            if isinstance(low, int) and isinstance(high, int):
                params[param] = np.random.randint(low, high + 1)
            else:
                params[param] = np.random.uniform(low, high)

        self.logger.debug(f"Simulating with parameters: {params}")

        # Perturb data if needed
        if perturb_data:
            data = self.data.copy()
            # Apply random noise to multiple price fields
            for price_field in ['Open', 'High', 'Low', 'Close']:
                if price_field in data.columns:
                    noise = np.random.normal(0, 0.01, size=len(data))  # 1% noise
                    data[price_field] *= (1 + noise)
            self.logger.debug("Data perturbed for simulation.")
        else:
            data = self.data

        # Run backtest with parameters
        try:
            key, output = self.backtest_runner.run_single_backtest(
                self.strategy_class,
                self.asset,
                self.data_dict,
                **params  # Pass parameters as keyword arguments
            )
            if output is not None:
                performance = output['_trades']['Equity'].iloc[-1]  # Final equity
                self.logger.debug(f"Performance for parameters {params}: {performance}")
                return {'params': params, 'performance': performance}
            else:
                self.logger.warning(f"Backtest output is None for parameters {params}.")
                return {'params': params, 'performance': None}
        except Exception as e:
            self.logger.error(f"Monte Carlo simulation failed with error: {e}")
            return {'params': params, 'performance': None}

    def optimize(self, param_ranges, n_simulations=100, perturb_data=False, max_cores=-1):
        """
        Perform Monte Carlo optimization.

        Parameters:
            param_ranges (dict): Dictionary of parameter ranges (low, high) for each parameter.
            n_simulations (int): Number of simulations to perform.
            perturb_data (bool): Whether to perturb the data.
            max_cores (int): Number of CPU cores to use (-1 for all available cores).

        Returns:
            tuple: (best_result, df_results)
        """
        self.logger.info("Starting Monte Carlo Optimization.")
        seeds = np.random.randint(0, 1e6, size=n_simulations)
        results = Parallel(n_jobs=max_cores)(
            delayed(self._simulate)(seed, param_ranges, perturb_data) for seed in seeds
        )
        df_results = pd.DataFrame(results)
        # Filter out failed simulations
        df_results = df_results.dropna(subset=['performance'])
        if df_results.empty:
            self.logger.error("All Monte Carlo simulations failed.")
            return None, df_results
        # Find the best parameters
        best_result = df_results.loc[df_results['performance'].idxmax()]
        self.logger.info(f"Best Monte Carlo Simulation Performance: {best_result['performance']}")
        return best_result, df_results
