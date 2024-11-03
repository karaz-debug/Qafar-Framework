# strategies/momentum_strategy.py

from .base_strategy import BaseStrategy
from backtesting.lib import crossover
import logging
import pandas as pd  # Ensure pandas is imported

def SMA(data, window):
    """
    Simple Moving Average (SMA) indicator.

    Parameters:
        data (pd.Series): Series of prices.
        window (int): The number of periods to calculate the SMA.

    Returns:
        pd.Series: The SMA values.
    """
    if not isinstance(data, pd.Series):
        logging.error(f"SMA function received data type: {type(data)} instead of pd.Series")
        return pd.Series([None]*len(data))
    return data.rolling(window=window).mean()

class MomentumStrategy(BaseStrategy):
    """
    A momentum-based strategy using short and long-term moving averages.
    Executes trades based on moving average crossovers on the primary timeframe.
    """

    # Strategy Parameters and Optimization Settings
    strategy_params = {
        'short_window': {'type': int, 'default': 20, 'prompt': 'Enter short moving average window (e.g., 20): '},
        'long_window': {'type': int, 'default': 100, 'prompt': 'Enter long moving average window (e.g., 100): '},
        'primary_tf': {'type': str, 'default': '5m', 'prompt': 'Enter primary timeframe (e.g., 5m): '},
        'sl_percent': {'type': float, 'default': 2.0, 'prompt': 'Enter stop-loss percentage (e.g., 2): '},
        'tp_percent': {'type': float, 'default': 4.0, 'prompt': 'Enter take-profit percentage (e.g., 4): '},
        'requires_multiple_timeframes': {'type': bool, 'default': False},
    }

    optimizable_params = ['short_window', 'long_window', 'sl_percent', 'tp_percent']

    def init(self):
        """
        Initialize moving averages on the primary timeframe using the custom SMA function.
        """
        logging.info(f"MomentumStrategy.init: self.data type: {type(self.data)}")

        try:
            # Access the underlying DataFrame for logging purposes
            df = self.data.df
            logging.info(f"MomentumStrategy.init: self.data.df columns: {df.columns}")
            logging.info(f"MomentumStrategy.init: self.data.df['Close'] type: {type(df['Close'])}")
            logging.info(f"MomentumStrategy.init: self.data.df['Close'] head:\n{df['Close'].head()}")
        except AttributeError as e:
            logging.error(f"Error accessing self.data.df: {e}")
            raise

        # Initialize short and long moving averages using the custom SMA function
        self.short_ma = self.I(SMA, self.data.df['Close'], self.short_window)
        self.long_ma = self.I(SMA, self.data.df['Close'], self.long_window)

        logging.info("Initialized short_ma and long_ma using SMA.")

    def next(self):
        """
        Execute the trading logic based on moving average crossover.
        """
        try:
            # Current close price accessed via the DataFrame
            current_close = self.data.df['Close'][-1]
            # Current moving average values
            current_short_ma = self.short_ma[-1]
            current_long_ma = self.long_ma[-1]

            logging.info(f"Current Close Price: {current_close}")
            logging.info(f"Short MA: {current_short_ma}, Long MA: {current_long_ma}")

            # Check for crossover conditions
            if crossover(self.short_ma, self.long_ma):
                self.buy(
                    sl=current_close * (1 - self.sl_percent / 100),  # Stop-loss percentage below current price
                    tp=current_close * (1 + self.tp_percent / 100)   # Take-profit percentage above current price
                )
                print(f'BUY signal triggered at {current_close}')
                logging.info(f"BUY signal triggered at {current_close}")
            elif crossover(self.long_ma, self.short_ma):
                self.sell(
                    sl=current_close * (1 + self.sl_percent / 100),  # Stop-loss percentage above current price
                    tp=current_close * (1 - self.tp_percent / 100)   # Take-profit percentage below current price
                )
                print(f'SELL signal triggered at {current_close}')
                logging.info(f"SELL signal triggered at {current_close}")
        except Exception as e:
            logging.error(f"Error in MomentumStrategy.next(): {e}")
