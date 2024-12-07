# src/technical_analysis.py

import pandas as pd
import ta

def apply_indicators(df):
    """
    Given a DataFrame with columns [time, open, high, low, close, volume],
    apply some technical indicators and return the same DataFrame with new indicator columns.
    """

    # Calculate RSI
    rsi_indicator = ta.momentum.RSIIndicator(close=df["close"], window=14)
    df["rsi"] = rsi_indicator.rsi()

    # Calculate a 50-period Exponential Moving Average (EMA)
    ema50_indicator = ta.trend.EMAIndicator(close=df["close"], window=50)
    df["ema50"] = ema50_indicator.ema_indicator()

    # Add any other indicators as needed
    return df
