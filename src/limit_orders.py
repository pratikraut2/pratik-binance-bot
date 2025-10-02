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
load_dotenv()  # load .env file
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    logging.error("Missing Binance API keys. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env")
    print("❌ ERROR: API keys not found. Check your .env file.")
    sys.exit(1)

# ==============================
# Initialize Client
# ==============================
# ⚠️ Use testnet=True for safe testing
client = Client(API_KEY, API_SECRET, testnet=True)


def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Places a LIMIT order on Binance Futures.
    :param symbol: Trading pair (e.g., 'BTCUSDT')
    :param side: BUY or SELL
    :param quantity: Order size
    :param price: Limit price
    """
    try:
        # Validate inputs
        if side.upper() not in ["BUY", "SELL"]:
            raise ValueError("Invalid side. Must be 'BUY' or 'SELL'.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        # Place order
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="LIMIT",
            timeInForce="GTC",  # Good-Til-Cancelled
            quantity=quantity,
            price=str(price)
        )
        logging.info(f"✅ Limit order placed: {order}")
        print(f"✅ Limit order placed successfully: {order}")
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
    if len(sys.argv) != 5:
        print("Usage: python src/limit_orders.py SYMBOL BUY/SELL QUANTITY PRICE")
        sys.exit(1)

    _, symbol, side, qty, price = sys.argv
    place_limit_order(symbol, side, float(qty), float(price))
