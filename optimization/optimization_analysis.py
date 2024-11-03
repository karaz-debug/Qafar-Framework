# optimization/optimization_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

class OptimizationAnalyzer:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def plot_heatmap(self, df: pd.DataFrame, x_param: str, y_param: str, metric: str, title: str, filename: str):
        """
        Generate and save a heatmap for the specified metric.
        """
        pivot_table = df.pivot(x_param, y_param, metric)
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap='viridis')
        plt.title(title)
        plt.xlabel(y_param.replace('_', ' ').title())
        plt.ylabel(x_param.replace('_', ' ').title())
        plt.savefig(filename)
        plt.close()
        self.logger.info(f"Heatmap '{title}' saved as '{filename}'")

    def generate_report(self, df_phase1: pd.DataFrame, df_phase2: pd.DataFrame, report_dir: str):
        """
        Generate a comprehensive report comparing Phase 1 and Phase 2 results.
        """
        self.logger.info("Generating comprehensive optimization report.")
        
        # Ensure report directory exists
        os.makedirs(report_dir, exist_ok=True)
        
        # Example: Compare top results from Phase 1 and Phase 2
        top_phase1 = df_phase1.nlargest(5, 'Primary Metric')
        top_phase2 = df_phase2.nlargest(5, 'Secondary Metric') if 'Secondary Metric' in df_phase2.columns else df_phase2
        
        # Save to text file
        report_file = os.path.join(report_dir, 'optimization_comparison_report.txt')
        with open(report_file, 'w') as f:
            f.write("Top 5 Results from Phase 1 (Maximize Primary Metric):\n")
            f.write(top_phase1.to_string(index=False))
            f.write("\n\nTop 5 Results from Phase 2 (Optimize Secondary Metrics):\n")
            f.write(top_phase2.to_string(index=False))
        
        self.logger.info(f"Comprehensive optimization report saved to '{report_file}'")
        
        # Save Best Parameters for Future Use
        best_phase1 = top_phase1.iloc[0].to_dict()
        best_phase2 = top_phase2.iloc[0].to_dict()
        best_params_file = os.path.join(report_dir, 'best_parameters.csv')
        pd.DataFrame([best_phase1, best_phase2]).to_csv(best_params_file, index=False)
        self.logger.info(f"Best parameters saved to '{best_params_file}'")
