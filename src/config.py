import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Add any other configuration parameters here later.
# For example, you might set the percentage of capital per trade:
TRADE_ALLOCATION_PERCENT = 0.05  # 5%
