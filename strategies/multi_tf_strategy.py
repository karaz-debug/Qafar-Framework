# strategies/multi_timeframe_strategy.py

from .base_strategy import BaseStrategy
import pandas as pd
import logging

class MultiTimeframeStrategy(BaseStrategy):
    """
    Multi-Timeframe Strategy.
    Buys when the higher timeframe trend is bullish and the current timeframe triggers a buy signal.
    Sells when the higher timeframe trend is bearish and the current timeframe triggers a sell signal.
    Executes trades on the primary (current) timeframe.
    """

    # Strategy Parameters and Optimization Settings
    strategy_params = {
        'higher_tf_short_ma': {'type': int, 'default': 5, 'prompt': 'Enter higher_tf_short_ma (e.g., 5): '},
        'higher_tf_long_ma': {'type': int, 'default': 10, 'prompt': 'Enter higher_tf_long_ma (e.g., 10): '},
        'current_tf_short_ma': {'type': int, 'default': 3, 'prompt': 'Enter current_tf_short_ma (e.g., 3): '},
        'current_tf_long_ma': {'type': int, 'default': 7, 'prompt': 'Enter current_tf_long_ma (e.g., 7): '},
        'primary_tf': {'type': str, 'default': '5m', 'prompt': 'Enter primary timeframe (e.g., 5m): '},
        'higher_tf': {'type': str, 'default': '1H', 'prompt': 'Enter higher timeframe (e.g., 1H): '},
        'sl_percent': {'type': float, 'default': 2.0, 'prompt': 'Enter stop-loss percentage (e.g., 2): '},
        'tp_percent': {'type': float, 'default': 4.0, 'prompt': 'Enter take-profit percentage (e.g., 4): '},
        'requires_multiple_timeframes': {'type': bool, 'default': True},
    }

    optimizable_params = [
        'higher_tf_short_ma',
        'higher_tf_long_ma',
        'current_tf_short_ma',
        'current_tf_long_ma',
        'sl_percent',
        'tp_percent'
    ]

    higher_tf_data = None  # Define as a class variable to receive data

    def init(self):
        """
        Initialize moving averages for both higher and current timeframes.
        """
        # Access higher timeframe data
        higher_tf_data = self.higher_tf_data
        if higher_tf_data is None:
            logging.error("Higher timeframe data 'higher_tf_data' not provided.")
            raise ValueError("Higher timeframe data 'higher_tf_data' not provided.")

        if not isinstance(higher_tf_data, pd.DataFrame):
            logging.error("Higher timeframe data 'higher_tf_data' is not a pandas DataFrame.")
            raise TypeError("Higher timeframe data 'higher_tf_data' is not a pandas DataFrame.")

        if 'Close' not in higher_tf_data.columns:
            logging.error("Close column missing in higher timeframe data 'higher_tf_data'.")
            raise ValueError("Close column missing in higher timeframe data 'higher_tf_data'.")

        # Compute higher timeframe moving averages and store in higher_tf_data
        self.higher_tf_data = higher_tf_data.copy()
        self.higher_tf_data['higher_short_ma'] = self.higher_tf_data['Close'].rolling(window=self.higher_tf_short_ma).mean()
        self.higher_tf_data['higher_long_ma'] = self.higher_tf_data['Close'].rolling(window=self.higher_tf_long_ma).mean()

        # Initialize a pointer to track the current higher timeframe index
        self.current_higher_index = 0

        # Initialize current timeframe moving averages using self.I() with lambda functions
        self.current_short_ma = self.I(lambda x: x.rolling(window=self.current_tf_short_ma).mean(), self.data.df['Close'])
        self.current_long_ma = self.I(lambda x: x.rolling(window=self.current_tf_long_ma).mean(), self.data.df['Close'])

        # Initialize previous higher_tf moving averages for crossover detection
        self.prev_higher_short_ma = None
        self.prev_higher_long_ma = None

        logging.info("Initialized higher and current timeframe moving averages.")

    def next(self):
        """
        Execute the trading logic based on higher and current timeframe indicators.
        """
        try:
            # Get current timestamp from primary timeframe
            current_timestamp = self.data.index[-1]
            logging.debug(f"Current timestamp: {current_timestamp}")

            # Advance higher_tf_index if the next higher_tf_data timestamp <= current_timestamp
            while (self.current_higher_index < len(self.higher_tf_data) - 1 and
                   self.higher_tf_data.index[self.current_higher_index + 1] <= current_timestamp):
                self.current_higher_index += 1
                logging.debug(f"Advanced higher_tf_index to {self.current_higher_index}")

            # Get current higher_tf moving averages
            higher_short_ma = self.higher_tf_data['higher_short_ma'].iloc[self.current_higher_index]
            higher_long_ma = self.higher_tf_data['higher_long_ma'].iloc[self.current_higher_index]
            logging.debug(f"Higher Short MA: {higher_short_ma}, Higher Long MA: {higher_long_ma}")

            # Check if moving averages are valid
            if pd.isna(higher_short_ma) or pd.isna(higher_long_ma):
                logging.debug("HTF moving averages are NaN, skipping signal generation.")
                return  # Not enough data to compute moving averages

            # Determine higher timeframe trend
            if self.prev_higher_short_ma is not None and self.prev_higher_long_ma is not None:
                higher_trend_bullish = (
                    self.prev_higher_short_ma < self.prev_higher_long_ma and
                    higher_short_ma > higher_long_ma
                )
                higher_trend_bearish = (
                    self.prev_higher_short_ma > self.prev_higher_long_ma and
                    higher_short_ma < higher_long_ma
                )
                logging.debug(f"Higher Trend Bullish: {higher_trend_bullish}, Higher Trend Bearish: {higher_trend_bearish}")
            else:
                higher_trend_bullish = False
                higher_trend_bearish = False
                logging.debug("No previous HTF moving averages to determine trend.")

            # Update previous higher_tf moving averages
            self.prev_higher_short_ma = higher_short_ma
            self.prev_higher_long_ma = higher_long_ma

            # Determine current timeframe signal using the last two values
            if len(self.current_short_ma) < 2 or len(self.current_long_ma) < 2:
                logging.debug("Not enough data to compute CTF signals.")
                return  # Not enough data to compute signals

            current_signal_buy = (
                self.current_short_ma[-2] < self.current_long_ma[-2] and
                self.current_short_ma[-1] > self.current_long_ma[-1]
            )
            current_signal_sell = (
                self.current_short_ma[-2] > self.current_long_ma[-2] and
                self.current_short_ma[-1] < self.current_long_ma[-1]
            )
            logging.debug(f"Current Signal Buy: {current_signal_buy}, Current Signal Sell: {current_signal_sell}")

            # Generate signals based on both timeframes
            current_close_price = self.data.df['Close'].iloc[-1]
            logging.debug(f"Current Close Price: {current_close_price}")

            if higher_trend_bullish and current_signal_buy:
                self.buy(
                    sl=current_close_price * (1 - self.sl_percent / 100),  # Stop-loss percentage below current price
                    tp=current_close_price * (1 + self.tp_percent / 100)   # Take-profit percentage above current price
                )
                logging.info(f"BUY signal at {current_close_price} based on multi-timeframe analysis")
                print(f'BUY signal triggered at {current_close_price} based on multi-timeframe analysis')
            elif higher_trend_bearish and current_signal_sell:
                self.sell(
                    sl=current_close_price * (1 + self.sl_percent / 100),  # Stop-loss percentage above current price
                    tp=current_close_price * (1 - self.tp_percent / 100)   # Take-profit percentage below current price
                )
                logging.info(f"SELL signal at {current_close_price} based on multi-timeframe analysis")
                print(f'SELL signal triggered at {current_close_price} based on multi-timeframe analysis')

        except Exception as e:
            logging.error(f"Error in MultiTimeframeStrategy.next(): {e}")
