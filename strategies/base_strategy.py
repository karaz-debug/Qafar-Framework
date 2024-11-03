# strategies/base_strategy.py

from backtesting import Strategy
import logging

class BaseStrategy(Strategy):
    """
    Base strategy class that handles additional keyword arguments and logging.
    """

    requires_multiple_timeframes = False  # Default to single-timeframe
    primary_tf = '1m'  # Default execution timeframe

    def init(self):
        """
        Initialize indicators and variables.
        Must be implemented by all derived strategy classes.
        """
        super().init()

    def next(self):
        """
        Define the trading logic.
        Must be implemented by all derived strategy classes.
        """
        pass
