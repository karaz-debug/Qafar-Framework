# backtest_framework/backtest/results_analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

class ResultsAnalyzer:
    """
    Analyzes and visualizes backtest results.
    """

    def __init__(self, results, report_dir='REPORT'):
        """
        Initialize with backtest results.

        Parameters:
            results (dict): Dictionary containing backtest results.
            report_dir (str): Directory where reports will be saved.
        """
        self.results = results
        self.report_dir = report_dir
        self._ensure_report_directory()

    def _ensure_report_directory(self):
        """
        Ensure that the report directory exists. Create it if it doesn't.
        """
        os.makedirs(self.report_dir, exist_ok=True)
        print(f"Report directory '{self.report_dir}' is ready.")

    def display_summary(self):
        """
        Display a summary of all backtest results.
        """
        if not self.results:
            print("No backtest results to display.")
            return

        summary = []
        for key, result in self.results.items():
            print(f"\nResult for '{key}':")
            if hasattr(result, '_trades') and not result._trades.empty:
                print("Available Trade Columns:", result._trades.columns.tolist())
                # Temporarily print the first few trades for inspection
                print(result._trades.head())
                
                # Safely list all attributes without causing AttributeError
                available_attrs = []
                for attr in dir(result):
                    if not attr.startswith('_'):
                        try:
                            attr_value = getattr(result, attr)
                            # Skip DataFrame and Series to avoid unhashable type error
                            if isinstance(attr_value, (pd.DataFrame, pd.Series)):
                                continue
                            # Skip callables
                            if callable(attr_value):
                                continue
                            available_attrs.append(attr)
                        except Exception as e:
                            print(f"Error accessing attribute '{attr}': {e}")
                            continue
                print("Available Result Attributes:", available_attrs)
                
                # Identify the correct column for win information
                if 'Win?' in result._trades.columns:
                    win_rate = result._trades['Win?'].mean() * 100
                elif 'PnL' in result._trades.columns:
                    win_rate = (result._trades['PnL'] > 0).mean() * 100
                elif 'ReturnPct' in result._trades.columns:
                    win_rate = (result._trades['ReturnPct'] > 0).mean() * 100
                else:
                    print("No suitable column found for Win Rate calculation.")
                    win_rate = 'N/A'

                total_trades = len(result._trades)

                # Attempt to access Max Drawdown and Avg Drawdown
                max_drawdown = getattr(result, 'Max Drawdown [%]', 'N/A')
                avg_drawdown = getattr(result, 'Avg Drawdown [%]', 'N/A')

                # If not found, compute manually
                if max_drawdown == 'N/A' or avg_drawdown == 'N/A':
                    equity_curve = getattr(result, '_equity_curve', None)
                    if equity_curve is not None and not equity_curve.empty:
                        # Calculate Max Drawdown
                        peak = equity_curve['Equity'].cummax()
                        drawdown = (peak - equity_curve['Equity']) / peak * 100
                        max_drawdown = drawdown.max()
                        avg_drawdown = drawdown.mean()
                        print(f"Computed Max Drawdown (%): {max_drawdown:.2f}")
                        print(f"Computed Avg Drawdown (%): {avg_drawdown:.2f}")
                    else:
                        print("No equity curve data available to compute drawdowns.")
            else:
                print("No trades data available.")
                total_trades = 'N/A'
                win_rate = 'N/A'
                max_drawdown = 'N/A'
                avg_drawdown = 'N/A'

            # Access attributes using getattr
            final_portfolio = getattr(result, 'Final Portfolio Value ($)', 'N/A')
            profit_factor = getattr(result, 'Profit Factor', 'N/A')
            sharpe_ratio = getattr(result, 'Sharpe Ratio', 'N/A')
            sortino_ratio = getattr(result, 'Sortino Ratio', 'N/A')
            calmar_ratio = getattr(result, 'Calmar Ratio', 'N/A')
            duration = getattr(result, 'Duration', 'N/A')
            start = getattr(result, 'Start', 'N/A')
            end = getattr(result, 'End', 'N/A')
            sqn = getattr(result, 'SQN', 'N/A')

            summary.append({
                'Strategy': key,
                'Final Portfolio Value ($)': final_portfolio,
                'Total Trades': total_trades,
                'Win Rate (%)': win_rate,
                'Profit Factor': profit_factor,
                'Max Drawdown (%)': max_drawdown,
                'Avg Drawdown (%)': avg_drawdown,
                'Sharpe Ratio': sharpe_ratio,
                'Sortino Ratio': sortino_ratio,
                'Calmar Ratio': calmar_ratio,
                'Duration': duration,
                'Start': start,
                'End': end,
                'SQN': sqn
            })

        summary_df = pd.DataFrame(summary)
        print("\nSummary of Backtest Results:")
        print(summary_df)


    def save_summary_to_csv(self, filename='backtest_summary.csv'):
        """
        Save the summary of backtest results to a CSV file.

        Parameters:
            filename (str): Name of the CSV file.
        """
        if not self.results:
            print("No backtest results to save.")
            return

        summary = []
        for key, result in self.results.items():
            # Derive Total Trades and Win Rate if not directly available
            if hasattr(result, '_trades') and not result._trades.empty:
                total_trades = len(result._trades)
                if 'Win?' in result._trades.columns:
                    win_rate = result._trades['Win?'].mean() * 100
                elif 'PnL' in result._trades.columns:
                    win_rate = (result._trades['PnL'] > 0).mean() * 100
                elif 'ReturnPct' in result._trades.columns:
                    win_rate = (result._trades['ReturnPct'] > 0).mean() * 100
                else:
                    win_rate = 'N/A'
            else:
                total_trades = 'N/A'
                win_rate = 'N/A'

            # Attempt to access Max Drawdown and Avg Drawdown
            max_drawdown = getattr(result, 'Max Drawdown [%]', 'N/A')
            avg_drawdown = getattr(result, 'Avg Drawdown [%]', 'N/A')

            # If not found, compute manually
            if max_drawdown == 'N/A' or avg_drawdown == 'N/A':
                equity_curve = getattr(result, '_equity_curve', None)
                if equity_curve is not None and not equity_curve.empty:
                    # Calculate Max Drawdown
                    peak = equity_curve['Equity'].cummax()
                    drawdown = (peak - equity_curve['Equity']) / peak * 100
                    max_drawdown = drawdown.max()
                    avg_drawdown = drawdown.mean()
                else:
                    max_drawdown = 'N/A'
                    avg_drawdown = 'N/A'

            # Access attributes using getattr
            final_portfolio = getattr(result, 'Final Portfolio Value ($)', 'N/A')
            profit_factor = getattr(result, 'Profit Factor', 'N/A')
            sharpe_ratio = getattr(result, 'Sharpe Ratio', 'N/A')
            sortino_ratio = getattr(result, 'Sortino Ratio', 'N/A')
            calmar_ratio = getattr(result, 'Calmar Ratio', 'N/A')
            duration = getattr(result, 'Duration', 'N/A')
            start = getattr(result, 'Start', 'N/A')
            end = getattr(result, 'End', 'N/A')
            sqn = getattr(result, 'SQN', 'N/A')

            summary.append({
                'Strategy': key,
                'Final Portfolio Value ($)': final_portfolio,
                'Total Trades': total_trades,
                'Win Rate (%)': win_rate,
                'Profit Factor': profit_factor,
                'Max Drawdown (%)': max_drawdown,
                'Avg Drawdown (%)': avg_drawdown,
                'Sharpe Ratio': sharpe_ratio,
                'Sortino Ratio': sortino_ratio,
                'Calmar Ratio': calmar_ratio,
                'Duration': duration,
                'Start': start,
                'End': end,
                'SQN': sqn
            })

        summary_df = pd.DataFrame(summary)
        csv_path = os.path.join(self.report_dir, filename)
        summary_df.to_csv(csv_path, index=False)
        print(f"Backtest summary saved to '{csv_path}'")

    def plot_equity_curve(self, strategy_key):
        """
        Plot the equity curve for a specific strategy.

        Parameters:
            strategy_key (str): The key identifying the strategy and asset (e.g., 'MomentumStrategy_BTCUSD').
        """
        if strategy_key in self.results:
            result = self.results[strategy_key]
            equity_curve = getattr(result, '_equity_curve', None)
            if equity_curve is not None and not equity_curve.empty:
                plt.figure(figsize=(10, 6))
                plt.plot(equity_curve.index, equity_curve['Equity'], label='Equity Curve')
                plt.title(f'Equity Curve - {strategy_key}')
                plt.xlabel('Time')
                plt.ylabel('Equity ($)')
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt_path = os.path.join(self.report_dir, f"{strategy_key}_equity_curve.png")
                plt.savefig(plt_path)
                plt.close()
                print(f"Equity curve plotted and saved to '{plt_path}'")
            else:
                print(f"No equity curve data available for '{strategy_key}'.")
        else:
            print(f"No results found for '{strategy_key}'")

    def generate_full_report(self, strategy_key, filename='report.html'):
        """
        Generate a full HTML report for a specific strategy.

        Parameters:
            strategy_key (str): The key identifying the strategy and asset.
            filename (str): Name of the HTML report file.
        """
        if strategy_key not in self.results:
            print(f"No results found for '{strategy_key}'")
            return

        result = self.results[strategy_key]
        equity_curve = getattr(result, '_equity_curve', None)
        trades = getattr(result, '_trades', None)

        # Generate Equity Curve Plot
        equity_plot_path = os.path.join(self.report_dir, f"{strategy_key}_equity_curve.png")
        if equity_curve is not None and not equity_curve.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(equity_curve.index, equity_curve['Equity'], label='Equity Curve')
            plt.title(f'Equity Curve - {strategy_key}')
            plt.xlabel('Time')
            plt.ylabel('Equity ($)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(equity_plot_path)
            plt.close()
        else:
            equity_plot_path = None

        # Prepare data for the template
        strategy_name = strategy_key
        equity_curve_img = os.path.basename(equity_plot_path) if equity_plot_path else ''

        # Prepare Performance Summary
        if hasattr(result, '_trades') and not result._trades.empty:
            total_trades = len(result._trades)
            if 'Win?' in result._trades.columns:
                win_rate = result._trades['Win?'].mean() * 100
            elif 'PnL' in result._trades.columns:
                win_rate = (result._trades['PnL'] > 0).mean() * 100
            elif 'ReturnPct' in result._trades.columns:
                win_rate = (result._trades['ReturnPct'] > 0).mean() * 100
            else:
                win_rate = 'N/A'

            # Attempt to access Max Drawdown and Avg Drawdown
            max_drawdown = getattr(result, 'Max Drawdown [%]', 'N/A')
            avg_drawdown = getattr(result, 'Avg Drawdown [%]', 'N/A')

            # If not found, compute manually
            if max_drawdown == 'N/A' or avg_drawdown == 'N/A':
                equity_curve = getattr(result, '_equity_curve', None)
                if equity_curve is not None and not equity_curve.empty:
                    # Calculate Max Drawdown
                    peak = equity_curve['Equity'].cummax()
                    drawdown = (peak - equity_curve['Equity']) / peak * 100
                    max_drawdown = drawdown.max()
                    avg_drawdown = drawdown.mean()
                else:
                    max_drawdown = 'N/A'
                    avg_drawdown = 'N/A'
        else:
            total_trades = 'N/A'
            win_rate = 'N/A'
            max_drawdown = 'N/A'
            avg_drawdown = 'N/A'

        # Access attributes using getattr
        final_portfolio = getattr(result, 'Final Portfolio Value ($)', 'N/A')
        profit_factor = getattr(result, 'Profit Factor', 'N/A')
        sharpe_ratio = getattr(result, 'Sharpe Ratio', 'N/A')
        sortino_ratio = getattr(result, 'Sortino Ratio', 'N/A')
        calmar_ratio = getattr(result, 'Calmar Ratio', 'N/A')
        duration = getattr(result, 'Duration', 'N/A')
        start = getattr(result, 'Start', 'N/A')
        end = getattr(result, 'End', 'N/A')
        sqn = getattr(result, 'SQN', 'N/A')
        return_pct = getattr(result, 'Return [%]', 'N/A')
        buy_hold_return = getattr(result, 'Buy & Hold Return [%]', 'N/A')
        annual_return = getattr(result, 'Return (Ann.) [%]', 'N/A')
        annual_volatility = getattr(result, 'Volatility (Ann.) [%]', 'N/A')

        # Format numeric values
        summary = {
            'Duration': duration,
            'Start': start,
            'End': end,
            'Return (%)': f"{return_pct:.2f}" if isinstance(return_pct, float) else return_pct,
            'Buy & Hold Return (%)': f"{buy_hold_return:.2f}" if isinstance(buy_hold_return, float) else buy_hold_return,
            'Return (Ann.) (%)': f"{annual_return:.2f}" if isinstance(annual_return, float) else annual_return,
            'Volatility (Ann.) (%)': f"{annual_volatility:.2f}" if isinstance(annual_volatility, float) else annual_volatility,
            'Sharpe Ratio': f"{sharpe_ratio:.2f}" if isinstance(sharpe_ratio, float) else sharpe_ratio,
            'Sortino Ratio': f"{sortino_ratio:.2f}" if isinstance(sortino_ratio, float) else sortino_ratio,
            'Calmar Ratio': f"{calmar_ratio:.2f}" if isinstance(calmar_ratio, float) else calmar_ratio,
            'Max Drawdown (%)': f"{max_drawdown:.2f}" if isinstance(max_drawdown, float) else max_drawdown,
            'Avg Drawdown (%)': f"{avg_drawdown:.2f}" if isinstance(avg_drawdown, float) else avg_drawdown,
            'Total Trades': total_trades,
            'Win Rate (%)': f"{win_rate:.2f}" if isinstance(win_rate, float) else win_rate,
            'Profit Factor': f"{profit_factor:.2f}" if isinstance(profit_factor, float) else profit_factor,
            'SQN': f"{sqn:.2f}" if isinstance(sqn, float) else sqn
        }

        summary_keys = list(summary.keys())
        summary_values = list(summary.values())

        # Convert trades DataFrame to HTML
        if trades is not None and not trades.empty:
            trades_html = trades.to_html(classes='dataframe', index=False)
        else:
            trades_html = "<p>No trades executed.</p>"
            
        # **Add the print statements here**
        print(f"Strategy Name: {strategy_name}")
        print(f"Equity Curve Image: {equity_curve_img}")
        print(f"Summary Keys: {summary_keys}")
        print(f"Summary Values: {summary_values}")
        print(f"Trades Table: {trades_html[:500]}")  # Print the first 500 characters

        # Set up Jinja2 environment
        # C:\Users\IQRA\Desktop\Qafary Framework\templates
        template_dir = r'C:/Users/IQRA/Desktop/Qafary Framework/templates'
        print(f"Looking for templates in: {template_dir}")  # Debugging line
        env = Environment(loader=FileSystemLoader(template_dir))
        try:
            template = env.get_template('report_template.html')
        except TemplateNotFound:
            print("Template 'report_template.html' not found in the 'templates' directory.")
            return

        # Render the template with context data
        try:
            html_content = template.render(
                strategy_name=strategy_name,
                equity_curve_img=equity_curve_img,
                summary_keys=summary_keys,
                summary_values=summary_values,
                trades_table=trades_html
            )
        except Exception as e:
            print(f"Error during template rendering: {e}")
            return

        # Save HTML Report
        report_path = os.path.join(self.report_dir, filename)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Full report generated and saved to '{report_path}'")

    def generate_performance_metrics(self, strategy_key):
        """
        Generate and print performance metrics for a specific strategy.

        Parameters:
            strategy_key (str): The key identifying the strategy and asset.
        """
        if strategy_key in self.results:
            result = self.results[strategy_key]
            # Derive Total Trades and Win Rate if not directly available
            if hasattr(result, '_trades') and not result._trades.empty:
                total_trades = len(result._trades)
                if 'Win?' in result._trades.columns:
                    win_rate = result._trades['Win?'].mean() * 100
                elif 'PnL' in result._trades.columns:
                    win_rate = (result._trades['PnL'] > 0).mean() * 100
                elif 'ReturnPct' in result._trades.columns:
                    win_rate = (result._trades['ReturnPct'] > 0).mean() * 100
                else:
                    win_rate = 'N/A'
            else:
                total_trades = 'N/A'
                win_rate = 'N/A'

            # Attempt to access Max Drawdown and Avg Drawdown
            max_drawdown = getattr(result, 'Max Drawdown [%]', 'N/A')
            avg_drawdown = getattr(result, 'Avg Drawdown [%]', 'N/A')

            # If not found, compute manually
            if max_drawdown == 'N/A' or avg_drawdown == 'N/A':
                equity_curve = getattr(result, '_equity_curve', None)
                if equity_curve is not None and not equity_curve.empty:
                    # Calculate Max Drawdown
                    peak = equity_curve['Equity'].cummax()
                    drawdown = (peak - equity_curve['Equity']) / peak * 100
                    max_drawdown = drawdown.max()
                    avg_drawdown = drawdown.mean()
                else:
                    max_drawdown = 'N/A'
                    avg_drawdown = 'N/A'

            # Access attributes using getattr
            final_portfolio = getattr(result, 'Final Portfolio Value ($)', 'N/A')
            profit_factor = getattr(result, 'Profit Factor', 'N/A')
            sharpe_ratio = getattr(result, 'Sharpe Ratio', 'N/A')
            sortino_ratio = getattr(result, 'Sortino Ratio', 'N/A')
            calmar_ratio = getattr(result, 'Calmar Ratio', 'N/A')
            duration = getattr(result, 'Duration', 'N/A')
            start = getattr(result, 'Start', 'N/A')
            end = getattr(result, 'End', 'N/A')
            sqn = getattr(result, 'SQN', 'N/A')

            metrics = {
                'Duration': duration,
                'Start': start,
                'End': end,
                'Return (%)': getattr(result, 'Return [%]', 'N/A'),
                'Buy & Hold Return (%)': getattr(result, 'Buy & Hold Return [%]', 'N/A'),
                'Return (Ann.) (%)': getattr(result, 'Return (Ann.) [%]', 'N/A'),
                'Volatility (Ann.) (%)': getattr(result, 'Volatility (Ann.) [%]', 'N/A'),
                'Sharpe Ratio': sharpe_ratio,
                'Sortino Ratio': sortino_ratio,
                'Calmar Ratio': calmar_ratio,
                'Max Drawdown (%)': max_drawdown,
                'Avg Drawdown (%)': avg_drawdown,
                'Total Trades': total_trades,
                'Win Rate (%)': win_rate,
                'Profit Factor': profit_factor,
                'SQN': sqn
            }

            # Print metrics in a nice format
            print(f"\nPerformance Metrics for '{strategy_key}':")
            for key, value in metrics.items():
                if isinstance(value, float):
                    print(f"{key}: {value:.2f}")
                else:
                    print(f"{key}: {value}")
            print("\n")
        else:
            print(f"No results found for '{strategy_key}'")
