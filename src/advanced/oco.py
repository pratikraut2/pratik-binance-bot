import logging
import os
import sys
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# ==============================
# Logging Setup
# ==============================
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ==============================
# Load API Keys from .env
# ==============================
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    logging.error("Missing Binance API keys. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env")
    print("❌ ERROR: API keys not found. Check your .env file.")
    sys.exit(1)

# ==============================
# Initialize Client (Testnet for safety)
# ==============================
client = Client(API_KEY, API_SECRET, testnet=True)


def place_oco_order(symbol: str, side: str, quantity: float, take_profit_price: float, stop_price: float):
    """
    Simulates an OCO order in Futures by placing:
    1. A TAKE-PROFIT order
    2. A STOP-MARKET order

    :param symbol: Trading pair (e.g., 'BTCUSDT')
    :param side: 'BUY' or 'SELL'
    :param quantity: Order quantity
    :param take_profit_price: Price for take-profit
    :param stop_price: Price for stop-loss
    """
    try:
        if side.upper() not in ["BUY", "SELL"]:
            raise ValueError("Invalid side. Must be 'BUY' or 'SELL'.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if take_profit_price <= 0 or stop_price <= 0:
            raise ValueError("Prices must be greater than 0.")

        opposite_side = "SELL" if side.upper() == "BUY" else "BUY"

        # Place Take-Profit order
        tp_order = client.futures_create_order(
            symbol=symbol.upper(),
            side=opposite_side,
            type="TAKE_PROFIT_MARKET",
            quantity=quantity,
            stopPrice=str(take_profit_price),
            timeInForce="GTC"
        )

        # Place Stop-Loss order
        sl_order = client.futures_create_order(
            symbol=symbol.upper(),
            side=opposite_side,
            type="STOP_MARKET",
            quantity=quantity,
            stopPrice=str(stop_price),
            timeInForce="GTC"
        )

        logging.info(f"✅ OCO (simulated) placed: TP={tp_order}, SL={sl_order}")
        print(f"✅ OCO order placed: Take-Profit at {take_profit_price}, Stop-Loss at {stop_price}")
        return {"take_profit": tp_order, "stop_loss": sl_order}

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
    if len(sys.argv) != 6:
        print("Usage: python src/advanced/oco.py SYMBOL BUY/SELL QUANTITY TAKE_PROFIT_PRICE STOP_PRICE")
        sys.exit(1)

    _, symbol, side, qty, tp_price, sl_price = sys.argv
    place_oco_order(symbol, side, float(qty), float(tp_price), float(sl_price))
