# src/main.py

from src.data_fetcher import get_24h_tickers, filter_pairs_by_volume, get_ohlc_data
from src.technical_analysis import apply_indicators
from src.strategy import generate_signal
from src.trade_executor import place_market_buy, place_market_sell
from src.account import compute_order_size_usdt, get_asset_balance
import schedule
import time
import logging

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

current_watchlist = []

def update_watchlist():
    print("Updating watchlist...")
    tickers = get_24h_tickers()
    global current_watchlist
    current_watchlist = filter_pairs_by_volume(tickers, min_volume=5000000)
    print("Current watchlist:", current_watchlist)

def analyze_and_decide():
    for symbol in current_watchlist:
        try:
            df = get_ohlc_data(symbol, interval='4h', limit=100)
            df = apply_indicators(df)
            action = generate_signal(df)
            logging.info(f"For {symbol}, signal is: {action}")

            if action == "buy":
                usdt_to_use = compute_order_size_usdt(0.05)  # 5%
                if usdt_to_use > 10:  # Ensure we have at least $10 to trade
                    logging.info(f"Placing a buy order on {symbol} for ${usdt_to_use} worth of {symbol}...")
                    order = place_market_buy(symbol, usdt_to_use)
                    logging.info(f"Buy order response: {order}")
            elif action == "sell":
                base_asset = symbol.replace('USDT', '')
                quantity = get_asset_balance(base_asset)
                if quantity > 0:
                    logging.info(f"Placing a sell order on {symbol} for {quantity} {base_asset}...")
                    order = place_market_sell(symbol, quantity)
                    logging.info(f"Sell order response: {order}")
                else:
                    logging.info(f"No {base_asset} to sell for {symbol}.")
        except Exception as e:
            logging.error(f"Error processing {symbol}: {e}")

def main():
    update_watchlist()
    # Schedule the watchlist update every 15 minutes
    schedule.every(15).minutes.do(update_watchlist)
    # Schedule analysis (every 2 hours)
    schedule.every(2).hours.do(analyze_and_decide)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
