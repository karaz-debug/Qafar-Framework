# strategies/breakout_mtf_strategy.py

from .base_strategy import BaseStrategy
import pandas as pd
import logging

class BreakoutMTFStrategy(BaseStrategy):
    """
    Multi-Timeframe Breakout Strategy.
    Buys when the price breaks above the higher timeframe resistance level and the higher timeframe trend is bullish.
    Sells when the price breaks below the higher timeframe support level and the higher timeframe trend is bearish.
    Executes trades on the primary (current) timeframe with defined Stop-Loss (SL) and Take-Profit (TP).
    """

    # Strategy Parameters and Optimization Settings
    strategy_params = {
        'tp_percent': {'type': float, 'default': 14, 'prompt': 'Enter take-profit percentage (e.g., 14): '},
        'sl_percent': {'type': float, 'default': 7, 'prompt': 'Enter stop-loss percentage (e.g., 7): '},
        'higher_tf_short_ma': {'type': int, 'default': 20, 'prompt': 'Enter higher_tf_short_ma (e.g., 20): '},
        'higher_tf_long_ma': {'type': int, 'default': 50, 'prompt': 'Enter higher_tf_long_ma (e.g., 50): '},
        'primary_tf': {'type': str, 'default': '5m', 'prompt': 'Enter primary timeframe (e.g., 5m): '},
        'higher_tf': {'type': str, 'default': '1H', 'prompt': 'Enter higher timeframe (e.g., 1H): '},
        'requires_multiple_timeframes': {'type': bool, 'default': True},
    }

    optimizable_params = ['tp_percent', 'sl_percent', 'higher_tf_short_ma', 'higher_tf_long_ma']

    # Define higher_tf_data as a class variable to receive data
    higher_tf_data = None

    def init(self):
        """
        Initialize indicators and align higher timeframe data.
        """
        super().init()  # Initialize base strategy

        logging.info("Initializing BreakoutMTFStrategy.")

        # Access higher timeframe data passed via BacktestRunner
        if self.higher_tf_data is None:
            logging.error("Higher timeframe data 'higher_tf_data' not provided.")
            raise ValueError("Higher timeframe data 'higher_tf_data' not provided.")

        if not isinstance(self.higher_tf_data, pd.DataFrame):
            logging.error("Higher timeframe data 'higher_tf_data' is not a pandas DataFrame.")
            raise TypeError("Higher timeframe data 'higher_tf_data' is not a pandas DataFrame.")

        required_columns = {'Close', 'support', 'resistance'}
        if not required_columns.issubset(self.higher_tf_data.columns):
            missing = required_columns - set(self.higher_tf_data.columns)
            logging.error(f"Required columns missing in higher timeframe data 'higher_tf_data': {missing}")
            raise ValueError(f"Required columns missing in higher timeframe data 'higher_tf_data': {missing}")

        # Calculate higher timeframe moving averages using parameters
        self.higher_short_ma = self.higher_tf_data['Close'].rolling(window=self.higher_tf_short_ma).mean()
        self.higher_long_ma = self.higher_tf_data['Close'].rolling(window=self.higher_tf_long_ma).mean()

        # Align higher timeframe support and resistance with primary timeframe using forward fill
        self.higher_support = self.higher_tf_data['support'].reindex(self.data.index, method='ffill')
        self.higher_resistance = self.higher_tf_data['resistance'].reindex(self.data.index, method='ffill')

        # Initialize index pointer for higher timeframe data
        self.current_higher_index = 0

        # Initialize previous higher timeframe moving averages for trend determination
        self.prev_higher_short_ma = None
        self.prev_higher_long_ma = None

        logging.info("BreakoutMTFStrategy initialized successfully.")

    def next(self):
        """
        Execute the trading logic on each new bar.
        """
        try:
            # Get the current timestamp from primary timeframe
            current_timestamp = self.data.index[-1]
            logging.debug(f"Current timestamp: {current_timestamp}")

            # Advance higher_tf_index if the next higher_tf_data timestamp <= current_timestamp
            while (self.current_higher_index < len(self.higher_short_ma) - 1 and
                   self.higher_tf_data.index[self.current_higher_index + 1] <= current_timestamp):
                self.current_higher_index += 1
                logging.debug(f"Advanced higher_tf_index to {self.current_higher_index}")

            # Get current higher_tf moving averages
            higher_short_ma = self.higher_short_ma.iloc[self.current_higher_index]
            higher_long_ma = self.higher_long_ma.iloc[self.current_higher_index]
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

            # Get current close price and HTF resistance/support
            current_close = self.data.Close[-1]
            hourly_resistance = self.higher_resistance.iloc[self.current_higher_index]
            hourly_support = self.higher_support.iloc[self.current_higher_index]
            logging.debug(f"Current Close: {current_close}, Hourly Resistance: {hourly_resistance}, Hourly Support: {hourly_support}")

            # Check for breakout above resistance
            if current_close > hourly_resistance and higher_trend_bullish:
                entry_price = current_close
                stop_loss = entry_price * (1 - self.sl_percent / 100)
                take_profit = entry_price * (1 + self.tp_percent / 100)

                # Ensure that SL and TP are logically placed
                if stop_loss < entry_price < take_profit:
                    logging.debug(f"Breakout Buy Signal: Entry={entry_price}, SL={stop_loss}, TP={take_profit}")
                    self.buy(sl=stop_loss, tp=take_profit)
                    logging.info(f"Executed BUY at {entry_price} with SL={stop_loss} and TP={take_profit}")

            # Check for breakout below support (Short Selling)
            if current_close < hourly_support and higher_trend_bearish:
                entry_price = current_close
                stop_loss = entry_price * (1 + self.sl_percent / 100)
                take_profit = entry_price * (1 - self.tp_percent / 100)

                # Ensure that SL and TP are logically placed
                if entry_price < stop_loss and take_profit < entry_price:
                    logging.debug(f"Breakout Sell Signal: Entry={entry_price}, SL={stop_loss}, TP={take_profit}")
                    self.sell(sl=stop_loss, tp=take_profit)
                    logging.info(f"Executed SELL at {entry_price} with SL={stop_loss} and TP={take_profit}")

        except Exception as e:
            logging.error(f"Error in BreakoutMTFStrategy.next(): {e}")
