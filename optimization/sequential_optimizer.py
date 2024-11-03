# optimization/sequential_optimizer.py

import itertools
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from backtest_framework.backtest.backtest_runner import BacktestRunner
import os

class SequentialOptimizer:
    def __init__(self, backtest_runner: BacktestRunner, logger: logging.Logger = None):
        self.backtest_runner = backtest_runner
        self.logger = logger or logging.getLogger(__name__)

    def optimize_phase1(self, primary_metric: str, param_grid: dict):
        """
        Phase 1: Optimize for the primary objective (e.g., maximize Equity Final [$]).
        """
        self.logger.info(f"Starting Phase 1 Optimization: {primary_metric}")
        
        # Generate all parameter combinations
        param_combinations = list(itertools.product(*param_grid.values()))
        param_names = list(param_grid.keys())
        
        results = []
        
        for params in param_combinations:
            param_dict = dict(zip(param_names, params))
            self.logger.info(f"Running backtest with parameters: {param_dict}")
            
            # Update strategy parameters
            for key, value in param_dict.items():
                setattr(self.backtest_runner.strategies[0], key, value)
            
            # Run backtest
            self.backtest_runner.run_backtests(concurrent=False)
            results_backtest = self.backtest_runner.get_results()
            result = results_backtest[list(results_backtest.keys())[0]]  # Assuming single strategy
            primary_value = result[primary_metric]
            
            # Store the results
            record = param_dict.copy()
            record['Primary Metric'] = primary_value
            for metric in ['Equity Final [$]', 'Sharpe Ratio', 'Calmar Ratio', 'Win Rate [%]', 'Max Drawdown [%]']:
                record[metric] = result.get(metric, None)
            results.append(record)
        
        df_results = pd.DataFrame(results)
        self.logger.info("Phase 1 Optimization Completed.")
        return df_results

    def optimize_phase2(self, df_phase1: pd.DataFrame, secondary_metrics: list, param_refinement: dict):
        """
        Phase 2: Optimize for secondary objectives based on user-specified metrics.
        Each metric in secondary_metrics should be a dictionary with 'metric' and 'direction' keys.
        Example:
            secondary_metrics = [
                {'metric': 'Max Drawdown [%]', 'direction': 'minimize'},
                {'metric': 'Sharpe Ratio', 'direction': 'maximize'}
            ]
        """
        for sec_metric in secondary_metrics:
            metric_name = sec_metric['metric']
            direction = sec_metric['direction']
            self.logger.info(f"Starting Phase 2 Optimization: {metric_name} ({direction})")
            
            # Select top N from Phase 1 based on primary metric
            top_n = param_refinement.get('top_n', 5)
            if direction == 'maximize':
                top_params = df_phase1.nlargest(top_n, 'Primary Metric')
            else:
                top_params = df_phase1.nsmallest(top_n, 'Primary Metric')
            
            # Define refined parameter grid based on top_params
            refined_param_grid = {}
            for key in param_refinement['refine_on']:
                # Extract the best range around the top parameters
                best_values = top_params[key]
                min_val = best_values.min() - param_refinement.get('refinement_step', 1)
                max_val = best_values.max() + param_refinement.get('refinement_step', 1)
                step = param_refinement.get('step', 1)
                # Ensure the range is valid (e.g., no negative values)
                min_val = max(min_val, 1)
                refined_param_grid[key] = range(int(min_val), int(max_val) + 1, step)
            
            # Generate all refined parameter combinations
            param_combinations = list(itertools.product(*refined_param_grid.values()))
            param_names = list(refined_param_grid.keys())
            
            results = []
            
            for params in param_combinations:
                param_dict = dict(zip(param_names, params))
                self.logger.info(f"Running Phase 2 backtest with parameters: {param_dict}")
                
                # Update strategy parameters
                for key, value in param_dict.items():
                    setattr(self.backtest_runner.strategies[0], key, value)
                
                # Run backtest
                self.backtest_runner.run_backtests(concurrent=False)
                results_backtest = self.backtest_runner.get_results()
                result = results_backtest[list(results_backtest.keys())[0]]  # Assuming single strategy
                sec_value = result[metric_name]
                
                # Store the results
                record = param_dict.copy()
                record['Secondary Metric'] = sec_value
                for metric in ['Equity Final [$]', 'Sharpe Ratio', 'Calmar Ratio', 'Win Rate [%]', 'Max Drawdown [%]']:
                    record[metric] = result.get(metric, None)
                results.append(record)
            
            df_results = pd.DataFrame(results)
            self.logger.info(f"Phase 2 Optimization for {metric_name} Completed.")
            return df_results

    def save_results(self, df_phase1: pd.DataFrame, df_phase2: pd.DataFrame, report_dir: str):
        """
        Save the optimization results to CSV files and generate heatmaps.
        """
        self.logger.info("Saving optimization results.")
        
        # Create directories for Phase 1 and Phase 2
        phase1_dir = os.path.join(report_dir, 'phase1')
        phase2_dir = os.path.join(report_dir, 'phase2')
        os.makedirs(phase1_dir, exist_ok=True)
        os.makedirs(phase2_dir, exist_ok=True)
        
        # Save Phase 1 results
        phase1_csv = os.path.join(phase1_dir, 'phase1_optimization_results.csv')
        df_phase1.to_csv(phase1_csv, index=False)
        self.logger.info(f"Phase 1 results saved to {phase1_csv}")
        
        # Save Phase 2 results
        phase2_csv = os.path.join(phase2_dir, 'phase2_optimization_results.csv')
        df_phase2.to_csv(phase2_csv, index=False)
        self.logger.info(f"Phase 2 results saved to {phase2_csv}")
        
        # Generate and save heatmaps for Phase 1
        self.generate_heatmap(df_phase1, 'tp_percent', 'sl_percent', 'Primary Metric', os.path.join(phase1_dir, 'phase1_heatmap.png'))
        
        # Generate and save heatmaps for Phase 2
        self.generate_heatmap(df_phase2, 'tp_percent', 'sl_percent', 'Secondary Metric', os.path.join(phase2_dir, 'phase2_heatmap.png'))

    def generate_heatmap(self, df: pd.DataFrame, x_param: str, y_param: str, metric: str, filename: str):
        """
        Generate and save a heatmap for the specified metric.
        """
        pivot_table = df.pivot(x_param, y_param, metric)
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title(f"Heatmap of {metric}")
        plt.xlabel(y_param.replace('_', ' ').title())
        plt.ylabel(x_param.replace('_', ' ').title())
        plt.savefig(filename)
        plt.close()
        self.logger.info(f"Heatmap for {metric} saved as {filename}")
