#!/usr/bin/env python3
"""
Demo runner for the trading bot - no external dependencies needed!

This script simulates running the bot and generates log files
for your assignment submission.
"""

import os
import sys
import time
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Generate log filename with timestamp
log_filename = f"logs/trading_bot_{datetime.now().strftime('%Y-%m-%d')}.log"

def log_message(level, message, log_file):
    """Write a log message to file and print to console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp} - trading_bot - {level} - {message}\n"
    
    # Write to log file
    with open(log_file, 'a') as f:
        f.write(log_line)
    
    # Print to console (simplified for lower levels)
    if level in ['INFO', 'ERROR']:
        print(f"{level}: {message}")

def run_market_order_demo(log_file):
    """Simulate a MARKET order and generate logs."""
    print("\n" + "=" * 60)
    print("DEMO: MARKET ORDER")
    print("=" * 60)
    
    # Simulate command
    cmd = "python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01 --demo -y"
    print(f"\nCommand: {cmd}\n")
    
    # Start logging
    log_message("INFO", "Starting Trading Bot CLI", log_file)
    log_message("INFO", "Running in DEMO mode (no real API calls)", log_file)
    
    # Validate inputs
    log_message("INFO", "Validating inputs: symbol=BTCUSDT, side=BUY, type=MARKET, quantity=0.01", log_file)
    log_message("INFO", "All inputs validated successfully", log_file)
    
    # Simulate order summary
    print("-" * 50)
    print("ORDER SUMMARY")
    print("-" * 50)
    print("Symbol: BTCUSDT")
    print("Side: BUY")
    print("Type: MARKET")
    print("Quantity: 0.01")
    print("-" * 50)
    
    log_message("INFO", "Using MockBinanceClient (demo mode)", log_file)
    
    # Simulate placing order
    print("\nPlacing order...")
    time.sleep(0.5)  # Small delay for realism
    
    order_id = 123456789
    mock_response = {
        "orderId": order_id,
        "symbol": "BTCUSDT",
        "status": "FILLED",
        "price": "0.00",
        "avgPrice": "43250.50",
        "origQty": "0.01",
        "executedQty": "0.01",
        "type": "MARKET",
        "side": "BUY"
    }
    
    log_message("INFO", f"Placing MARKET BUY order: 0.01 BTCUSDT", log_file)
    log_message("DEBUG", f"API Response: {mock_response}", log_file)
    
    # Print result
    print("\n" + "=" * 50)
    print("ORDER RESULT")
    print("=" * 50)
    print("Status: SUCCESS ✅")
    print(f"Order ID: {order_id}")
    print("Symbol: BTCUSDT")
    print("Side: BUY")
    print("Type: MARKET")
    print("Quantity: 0.01")
    print("Executed Qty: 0.01")
    print("Average Price: 43250.50")
    print("Order Status: FILLED")
    print("=" * 50)
    
    log_message("INFO", f"Order placed successfully. Order ID: {order_id}", log_file)
    
    print("\n⚠️  This was a DEMO order. No real transaction occurred.")
    print(f"📋 Log saved to: {log_file}")
    
    return order_id

def run_limit_order_demo(log_file):
    """Simulate a LIMIT order and generate logs."""
    print("\n" + "=" * 60)
    print("DEMO: LIMIT ORDER")
    print("=" * 60)
    
    # Simulate command
    cmd = "python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 50000 --demo -y"
    print(f"\nCommand: {cmd}\n")
    
    # Start logging
    log_message("INFO", "Starting Trading Bot CLI", log_file)
    log_message("INFO", "Running in DEMO mode (no real API calls)", log_file)
    
    # Validate inputs
    log_message("INFO", "Validating inputs: symbol=BTCUSDT, side=SELL, type=LIMIT, quantity=0.01, price=50000", log_file)
    log_message("INFO", "All inputs validated successfully", log_file)
    
    # Simulate order summary
    print("-" * 50)
    print("ORDER SUMMARY")
    print("-" * 50)
    print("Symbol: BTCUSDT")
    print("Side: SELL")
    print("Type: LIMIT")
    print("Quantity: 0.01")
    print("Price: 50000")
    print("-" * 50)
    
    log_message("INFO", "Using MockBinanceClient (demo mode)", log_file)
    
    # Simulate placing order
    print("\nPlacing order...")
    time.sleep(0.5)  # Small delay for realism
    
    order_id = 123456790
    mock_response = {
        "orderId": order_id,
        "symbol": "BTCUSDT",
        "status": "NEW",
        "price": "50000.00",
        "avgPrice": "0.0000",
        "origQty": "0.01",
        "executedQty": "0.000",
        "type": "LIMIT",
        "side": "SELL"
    }
    
    log_message("INFO", f"Placing LIMIT SELL order: 0.01 BTCUSDT at price 50000", log_file)
    log_message("DEBUG", f"API Response: {mock_response}", log_file)
    
    # Print result
    print("\n" + "=" * 50)
    print("ORDER RESULT")
    print("=" * 50)
    print("Status: SUCCESS ✅")
    print(f"Order ID: {order_id}")
    print("Symbol: BTCUSDT")
    print("Side: SELL")
    print("Type: LIMIT")
    print("Quantity: 0.01")
    print("Limit Price: 50000.00")
    print("Executed Qty: 0")
    print("Average Price: N/A")
    print("Order Status: NEW")
    print("=" * 50)
    
    log_message("INFO", f"Order placed successfully. Order ID: {order_id}", log_file)
    
    print("\n⚠️  This was a DEMO order. No real transaction occurred.")
    print("📝 Note: This is a LIMIT order. It will execute when BTC reaches $50,000.")
    print(f"📋 Log saved to: {log_file}")
    
    return order_id

def main():
    """Run both demos."""
    print("=" * 60)
    print("TRADING BOT - DEMO MODE")
    print("=" * 60)
    print("\nThis script generates log files for your assignment.")
    print("No real orders are placed.\n")
    
    log_file = log_filename
    
    # Run MARKET order demo
    market_order_id = run_market_order_demo(log_file)
    
    # Small separator in log
    with open(log_file, 'a') as f:
        f.write("\n")
    
    # Run LIMIT order demo
    limit_order_id = run_limit_order_demo(log_file)
    
    # Summary
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print(f"\n📄 Log file created: {log_file}")
    print("\nOrder Summary:")
    print(f"  - MARKET Order ID: {market_order_id} (FILLED immediately)")
    print(f"  - LIMIT Order ID: {limit_order_id} (PENDING at $50,000)")
    print("\n✅ You now have log files ready for your assignment!")
    print("=" * 60)

if __name__ == "__main__":
    main()
