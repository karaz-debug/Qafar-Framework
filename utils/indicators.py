# utils/indicators.py

import pandas as pd

def calculate_moving_average(close_prices: pd.Series, window: int) -> pd.Series:
    """
    Calculate the moving average for a given window size.

    Parameters:
        close_prices (pd.Series): Series of 'Close' prices.
        window (int): Window size for the moving average.

    Returns:
        pd.Series: Calculated moving average.
    """
    return close_prices.rolling(window=window).mean()

def calculate_support_resistance(data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Calculate support and resistance levels based on rolling min and max.

    Parameters:
        data (pd.DataFrame): DataFrame containing 'Close' prices.
        window (int): Window size for calculating support and resistance.

    Returns:
        pd.DataFrame: DataFrame with added 'support' and 'resistance' columns.
    """
    data['support'] = data['Close'].rolling(window=window).min()
    data['resistance'] = data['Close'].rolling(window=window).max()
    return data
