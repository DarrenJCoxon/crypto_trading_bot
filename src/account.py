# src/account.py

from binance.client import Client
from src.config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

def get_usdt_balance():
    """
    Fetch the user's USDT balance from Binance.
    Returns a float indicating the free amount of USDT.
    """
    account_info = client.get_account()
    balances = account_info.get('balances', [])
    for asset in balances:
        if asset['asset'] == 'USDT':
            return float(asset['free'])
    return 0.0

def compute_order_size_usdt(percentage=0.05):
    """
    Compute how much USDT to allocate based on a percentage of current balance.
    Default is 5% (0.05).
    """
    total_usdt = get_usdt_balance()
    return total_usdt * percentage

def get_asset_balance(asset):
    """
    Fetch the user's balance for a specific asset.
    Returns the free amount of the asset.
    """
    account_info = client.get_account()
    balances = account_info.get('balances', [])
    for item in balances:
        if item['asset'] == asset:
            return float(item['free'])
    return 0.0
