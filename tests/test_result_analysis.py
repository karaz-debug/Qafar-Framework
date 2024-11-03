# test_results_analysis.py

from backtest_framework.backtest.results_analysis import ResultsAnalyzer
import pandas as pd

# Mock backtest result
mock_result = {
    'MomentumStrategy_BTCUSD': pd.Series({
        'Duration': '1506 days 08:15:00',
        'Start': '2020-08-31 21:00:00',
        'End': '2024-10-16 05:15:00',
        'Return [%]': -82.826091,
        'Buy & Hold Return [%]': 474.691741,
        'Return (Ann.) [%]': -34.716134,
        'Volatility (Ann.) [%]': 20.34246,
        'Sharpe Ratio': 0.0,
        'Sortino Ratio': 0.0,
        'Calmar Ratio': 0.0,
        'Max. Drawdown [%]': -84.626626,
        'Avg. Drawdown [%]': -3.761489,
        '# Trades': 2536,
        'Win Rate [%]': 27.444795,
        'Profit Factor': 0.868697,
        'SQN': -2.133084,
        '_equity_curve': pd.DataFrame({
            'Equity': [10000, 10500, 10300, 11000, 10800]
        }, index=pd.date_range(start='2020-08-31', periods=5, freq='D')),
        '_trades': pd.DataFrame({
            'Size': [1, -1, 1],
            'Entry': [10000, 10500, 10300],
            'Exit': [10500, 10300, 11000],
            'Profit': [500, -200, 700]
        })
    })
}

# Initialize and run analyzer
analyzer = ResultsAnalyzer(mock_result, report_dir='TEST_REPORT')
analyzer.display_summary()
analyzer.save_summary_to_csv()
analyzer.plot_equity_curve('MomentumStrategy_BTCUSD')
analyzer.generate_full_report('MomentumStrategy_BTCUSD', filename='MomentumStrategy_BTCUSD_Test_Report.html')
