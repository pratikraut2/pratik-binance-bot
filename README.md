# Binance Futures Order Bot

## 📌 Objective
A CLI-based trading bot for Binance USDT-M Futures supporting:
- Market Orders
- Limit Orders
- Advanced Orders (OCO, TWAP)

## 📂 Project Structure
src/
├── market_orders.py
├── limit_orders.py
└── advanced/
├── oco.py
├── twap.py
bot.log
report.pdf
README.md


## ⚙️ Setup
1. Install dependencies:
   ```bash
   pip install python-binance



---

## ⚙️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/binance-futures-bot.git
cd binance-futures-bot

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
pip install python-binance
pip install reportlab      # for PDF reports

```
### 2. Configure API Keys
Create a `.env` file in the root directory and add your Binance API credentials:
```

BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

```
### 3. Run the Bot
```bash
python src/market_orders.py
python src/limit_orders.py
python src/advanced/oco.py
python src/advanced/twap.py
```
```
### 4. Logging
All activities are logged in `bot.log` for monitoring and debugging.
### 5. Reporting
Trade summaries and performance reports are generated in `report.pdf`.
```
## 🛠️ Usage
### Market Orders
```bash
python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001
```
### Limit Orders
```bash
python src/limit_orders.py --symbol BTCUSDT --side SELL --quantity 0.001 --price 50000
```
### OCO Orders
```bash
python src/advanced/oco.py --symbol BTCUSDT --side SELL --quantity 0.001 --price 55000 --stopPrice 48000
```
### TWAP Orders
```bash
python src/advanced/twap.py --symbol BTCUSDT --side BUY --quantity 0.01 --interval 60 --duration 3600
```
