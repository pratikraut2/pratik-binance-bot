import logging
import os
import sys
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException


logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ==============================
# Load API Keys from .env
# ==============================
load_dotenv()  # Load from .env
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    logging.error("Missing Binance API keys. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env")
    print("❌ ERROR: API keys not found. Check your .env file.")
    sys.exit(1)


client = Client(API_KEY, API_SECRET, testnet=True)


def place_market_order(symbol: str, side: str, quantity: float):
    """
    Places a market order on Binance Futures.
    :param symbol: Trading pair (e.g., 'BTCUSDT')
    :param side: 'BUY' or 'SELL'
    :param quantity: Order quantity
    """
    try:
        # Validate inputs
        if side.upper() not in ["BUY", "SELL"]:
            raise ValueError("Invalid side. Must be 'BUY' or 'SELL'.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        # Place order
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        logging.info(f"✅ Market order placed: {order}")
        print(f"✅ Market order placed successfully: {order}")
        return order

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        print(f"❌ Validation error: {ve}")
        return None

    except BinanceAPIException as be:
        logging.error(f"Binance API error: {be}")
        print(f"❌ Binance API error: {be}")
        return None

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        return None


# ==============================
# CLI Entry Point
# ==============================
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python src/market_orders.py SYMBOL BUY/SELL QUANTITY")
        sys.exit(1)

    _, symbol, side, qty = sys.argv
    place_market_order(symbol, side, float(qty))
