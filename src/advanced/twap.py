import logging
import os
import sys
import time
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException


logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    logging.error("Missing Binance API keys. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env")
    print("❌ ERROR: API keys not found. Check your .env file.")
    sys.exit(1)


client = Client(API_KEY, API_SECRET, testnet=True)


def place_twap_order(symbol: str, side: str, total_qty: float, intervals: int, delay: int):
    """
    TWAP strategy: split large order into smaller market orders executed over time.
    :param symbol: Trading pair (e.g., 'BTCUSDT')
    :param side: BUY or SELL
    :param total_qty: Total quantity to trade
    :param intervals: Number of smaller orders
    :param delay: Delay (seconds) between each order
    """
    try:
        # Input validation
        if side.upper() not in ["BUY", "SELL"]:
            raise ValueError("Invalid side. Must be 'BUY' or 'SELL'.")

        if total_qty <= 0:
            raise ValueError("Total quantity must be greater than 0.")

        if intervals <= 0:
            raise ValueError("Intervals must be greater than 0.")

        if delay < 0:
            raise ValueError("Delay must be >= 0 seconds.")

        qty_per_order = round(total_qty / intervals, 5)

        for i in range(intervals):
            try:
                order = client.futures_create_order(
                    symbol=symbol.upper(),
                    side=side.upper(),
                    type="MARKET",
                    quantity=qty_per_order
                )
                logging.info(f"✅ TWAP order {i+1}/{intervals} placed: {order}")
                print(f"✅ TWAP order {i+1}/{intervals} placed successfully")
                if i < intervals - 1:  # Don't sleep after last order
                    time.sleep(delay)
            except BinanceAPIException as be:
                logging.error(f"Binance API error on TWAP order {i+1}: {be}")
                print(f"❌ Binance API error on TWAP order {i+1}: {be}")
                break
            except Exception as e:
                logging.error(f"Unexpected error on TWAP order {i+1}: {e}")
                print(f"❌ Unexpected error on TWAP order {i+1}: {e}")
                break

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        print(f"❌ Validation error: {ve}")
    except Exception as e:
        logging.error(f"Unexpected TWAP setup error: {e}")
        print(f"❌ Unexpected TWAP setup error: {e}")


# ==============================
# CLI Entry Point
# ==============================
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python src/advanced/twap.py SYMBOL BUY/SELL TOTAL_QTY INTERVALS DELAY")
        sys.exit(1)

    _, symbol, side, total_qty, intervals, delay = sys.argv
    place_twap_order(symbol, side, float(total_qty), int(intervals), int(delay))
