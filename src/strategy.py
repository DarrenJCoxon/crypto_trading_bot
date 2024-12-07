# src/strategy.py

def generate_signal(df):
    """
    Given a DataFrame with OHLC data and indicators, 
    return "buy", "sell", or "hold" based on simplistic logic.
    """
    # Check the latest row
    latest = df.iloc[-1]

    if latest["close"] > latest["ema50"] and latest["rsi"] < 30:
        return "buy"
    elif latest["close"] < latest["ema50"] or latest["rsi"] > 70:
        return "sell"
    else:
        return "hold"
