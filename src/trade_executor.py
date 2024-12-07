# src/trade_executor.py

from binance.client import Client
from src.config import BINANCE_API_KEY, BINANCE_API_SECRET
from src.account import compute_order_size_usdt
import math

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

def place_market_buy(symbol, usdt_amount):
    """
    Place a market buy order for a given USDT amount on the specified symbol.
    Steps:
    1. Get the current price of the symbol.
    2. Compute the quantity to buy = usdt_amount / current_price.
    3. Round the quantity to comply with Binance lot size rules.
    4. Place a market buy order.
    """
    # Get current ticker price for the symbol
    ticker = client.get_symbol_ticker(symbol=symbol)
    price = float(ticker['price'])

    # Compute quantity
    quantity = usdt_amount / price

    # Binance has rules on min order size and step sizes. 
    # For simplicity, we try a simple rounding. For production, 
    # you'd fetch exchangeInfo and round properly based on symbol filters.
    quantity = round(quantity, 6)  # 6 decimal places as an example

    # Place market order
    order = client.create_order(
        symbol=symbol,
        side='BUY',
        type='MARKET',
        quantity=quantity
    )

    return order

def place_market_sell(symbol, quantity):
    """
    Place a market sell order for a given quantity of the base asset.
    """
    # Just a direct market sell
    # Again, ensure quantity is rounded properly.
    quantity = round(quantity, 6)
    
    order = client.create_order(
        symbol=symbol,
        side='SELL',
        type='MARKET',
        quantity=quantity
    )

    return order
