# src/data_fetcher.py

from binance.client import Client
from src.config import BINANCE_API_KEY, BINANCE_API_SECRET
import pandas as pd

# Initialize the Binance client
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

def get_all_tickers():
    """
    Fetches the latest price for all symbols.
    Returns a list of dicts, each dict contains 'symbol' and 'price'.
    """
    return client.get_all_tickers()

def get_24h_tickers():
    """
    Fetch 24-hour ticker data for all symbols.
    This includes volume, price change, and other stats.
    Returns a list of dicts, each dict includes fields like:
    'symbol', 'priceChange', 'priceChangePercent', 'weightedAvgPrice', 
    'prevClosePrice', 'lastPrice', 'lastQty', 'bidPrice', 'askPrice', 
    'openPrice', 'highPrice', 'lowPrice', 'volume', 'quoteVolume', etc.
    """
    return client.get_ticker()

def filter_pairs_by_volume(tickers, min_volume=1000000):
    """
    Given a list of 24h ticker data, filter out symbols that do not meet 
    the minimum volume criteria.
    Assumes trading against USDT and uses 'quoteVolume' field to filter.
    Returns a list of symbols that meet the criteria.
    """
    filtered = []
    for t in tickers:
        # Only consider pairs ending in 'USDT'
        if t['symbol'].endswith('USDT'):
            quote_volume = float(t.get('quoteVolume', 0.0))
            if quote_volume >= min_volume:
                filtered.append(t['symbol'])
    return filtered

def get_ohlc_data(symbol, interval='4h', limit=100):
    """
    Fetch historical OHLCV data (candlesticks) for a given symbol and interval.
    The default interval is 4 hours and default limit is 100 candles.
    
    Returns a pandas DataFrame with columns:
    time, open, high, low, close, volume
    """
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades", "taker_base_vol", 
        "taker_quote_vol", "ignore"
    ])

    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    # Convert open_time to a readable datetime
    df["time"] = pd.to_datetime(df["open_time"], unit='ms')

    # Keep only essential columns
    df = df[["time", "open", "high", "low", "close", "volume"]]

    return df
