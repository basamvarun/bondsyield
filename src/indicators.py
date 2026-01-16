import pandas as pd
import numpy as np


def calculate_spreads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yield curve spreads:
    - 2Y–10Y
    - 1Y–10Y
    """
    df = df.copy()
    if "10Y" in df.columns and "2Y" in df.columns:
        df["spread_2y_10y"] = df["10Y"] - df["2Y"]

    if "10Y" in df.columns and "1Y" in df.columns:
        df["spread_1y_10y"] = df["10Y"] - df["1Y"]

    return df


def calculate_volatility(series: pd.Series, window: int = 20) -> pd.Series:
    """
    Rolling volatility (standard deviation).
    Measures uncertainty in yield movements.
    """
    return series.rolling(window).std()


def calculate_zscore(series: pd.Series, window: int = 60) -> pd.Series:
    """
    Z-score of yield relative to its rolling mean.
    Indicates statistical extremes.
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std
