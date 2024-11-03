# strategies/__init__.py

from .base_strategy import BaseStrategy
from .momentum_strategy import MomentumStrategy
from .multi_tf_strategy import MultiTimeframeStrategy
from .breakout_strategy import BreakoutMTFStrategy

# The __all__ list defines the public interface of the package, making these classes accessible when importing the strategies package.
__all__ = ['BaseStrategy', 'MomentumStrategy', 'MultiTimeframeStrategy', 'BreakoutMTFStrategy']
