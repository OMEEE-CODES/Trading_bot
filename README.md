# Trading Bot - Binance Futures Testnet

A simple Python trading bot for placing orders on Binance Futures Testnet (USDT-M).

## Features

- ✅ Place **MARKET** orders (buy/sell at current market price)
- ✅ Place **LIMIT** orders (buy/sell at a specific price)
- ✅ Input validation with clear error messages
- ✅ Logging of all API requests and responses
- ✅ Clean, modular code structure
- ✅ Simple CLI interface

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance API client wrapper
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation
│   └── logging_config.py    # Logging setup
├── cli.py                   # CLI entry point
├── .env                     # Environment variables (API keys)
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Create a Binance Futures Testnet Account

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Generate your API Key and Secret

### 2. Install Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure API Credentials

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API credentials
# BINANCE_API_KEY=your_api_key_here
# BINANCE_API_SECRET=your_api_secret_here
```

**⚠️ Important:** Never commit your `.env` file to version control. It's already added to `.gitignore`.

## Demo Mode (No API Keys Required!)

Want to test the bot without setting up API keys? Use **demo mode**:

```bash
# Generate sample log files with demo orders
python3 run_demo.py

# Or use the CLI with --demo flag
python3 cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01 --demo -y

# Demo mode with LIMIT order
python3 cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 50000 --demo -y
```

Demo mode uses a mock client that simulates API responses - no real orders are placed!

### Demo Mode Options

| Option | Description |
|--------|-------------|
| `--demo`, `-d` | Run in demo mode (no real API calls) |
| `--auto-confirm`, `-y` | Skip confirmation prompt |

## Usage

### Place a MARKET Order

Market orders are executed immediately at the current market price.

```bash
# Buy 0.01 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01

# Sell 0.01 BTC at market price
python cli.py --symbol BTCUSDT --side SELL --order-type MARKET --quantity 0.01
```

### Place a LIMIT Order

Limit orders are executed only when the market reaches your specified price.

```bash
# Sell 0.01 BTC at $50,000 (order executes if price reaches 50000)
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 50000

# Buy 0.01 BTC at $40,000 (order executes if price drops to 40000)
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 40000
```

### Command Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--symbol` | `-s` | Yes | Trading pair (e.g., BTCUSDT, ETHUSDT) |
| `--side` | | Yes | BUY or SELL |
| `--order-type` | `-t` | Yes | MARKET or LIMIT |
| `--quantity` | `-q` | Yes | Order quantity (e.g., 0.01) |
| `--price` | `-p` | For LIMIT | Order price (required for LIMIT orders) |
| `--log-file` | | No | Custom log file path |

## Examples

```bash
# Example 1: Market Buy Order
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01

# Example 2: Market Sell Order
python cli.py --symbol ETHUSDT --side SELL --order-type MARKET --quantity 0.1

# Example 3: Limit Buy Order
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 40000

# Example 4: Limit Sell Order
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.1 --price 3000
```

## Logging

All API requests, responses, and errors are logged to a file. By default, log files are named `trading_bot_YYYY-MM-DD.log`.

To specify a custom log file:
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01 --log-file my_log.txt
```

## Output Example

```
--------------------------------------------------
ORDER SUMMARY
--------------------------------------------------
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01
--------------------------------------------------

Do you want to place this order? (yes/no): yes

==================================================
ORDER RESULT
==================================================
Status: SUCCESS
Order ID: 123456789
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01
Executed Qty: 0.01
Average Price: 43250.50
Order Status: FILLED
==================================================
```

## Error Handling

The bot validates all inputs before sending to the API:

- Symbol format (must be uppercase, e.g., BTCUSDT)
- Order side (BUY or SELL only)
- Order type (MARKET or LIMIT only)
- Quantity (must be a positive number)
- Price (required for LIMIT orders)

Common errors and solutions:

| Error | Solution |
|-------|----------|
| "API credentials not found" | Check your `.env` file has correct API key and secret |
| "Invalid symbol format" | Use uppercase letters only (e.g., BTCUSDT not btcusdt) |
| "Price is required for LIMIT orders" | Add `--price` parameter for LIMIT orders |
| "Price should not be provided for MARKET orders" | Remove `--price` for MARKET orders |

## Assumptions

1. **Testnet Only**: This bot is designed for Binance Futures Testnet only. Do not use production API keys.
2. **USDT-M Futures**: Only USDT-margined futures are supported.
3. **Minimum Order Size**: Binance has minimum order sizes. For BTC, it's typically 0.001 BTC.
4. **Testnet Funds**: You need testnet funds in your account to place orders. Get testnet funds from the Binance Testnet interface.

## Technologies Used

- **Python 3.x**: Core language
- **requests**: For HTTP API calls
- **python-dotenv**: For environment variable management
- **Standard library**: argparse, logging, hmac, hashlib

## Troubleshooting

### "Could not connect to Binance API"
- Check your internet connection
- Verify your API key and secret are correct
- Ensure you're using Testnet credentials, not production

### "Insufficient margin"
- You need testnet funds in your account
- Get testnet funds from: https://testnet.binancefuture.com

### "Invalid API key"
- Generate new API keys from the testnet
- Make sure you're using the testnet, not the main Binance website

## License

This project is for educational purposes as part of a Python internship assignment.

## Author

Created for Python Developer Internship Assignment.
# Trading_bot
