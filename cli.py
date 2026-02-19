#!/usr/bin/env python3
"""
CLI Entry Point for the Trading Bot.

This script provides a command-line interface for placing orders
on Binance Futures Testnet.

Examples:
    # Place a MARKET order
    python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01

    # Place a LIMIT order
    python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 50000
    
    # Run in demo mode (no real API calls)
    python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01 --demo
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from bot.client import BinanceClient, MockBinanceClient
from bot.orders import OrderManager
from bot.validators import validate_all_inputs
from bot.logging_config import setup_logging


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures Testnet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Market order (buy 0.01 BTC)
  python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
  
  # Limit order (sell 0.01 BTC at $50,000)
  python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 50000
  
  # Demo mode (no real orders)
  python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01 --demo
        """
    )
    
    parser.add_argument(
        '--symbol', '-s',
        required=True,
        help='Trading pair symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        '--side',
        required=True,
        choices=['BUY', 'SELL', 'buy', 'sell'],
        help='Order side: BUY or SELL'
    )
    
    parser.add_argument(
        '--order-type', '-t',
        required=True,
        choices=['MARKET', 'LIMIT', 'market', 'limit'],
        help='Order type: MARKET or LIMIT'
    )
    
    parser.add_argument(
        '--quantity', '-q',
        required=True,
        help='Order quantity (e.g., 0.01)'
    )
    
    parser.add_argument(
        '--price', '-p',
        help='Order price (required for LIMIT orders)'
    )
    
    parser.add_argument(
        '--log-file',
        help='Path to log file (default: trading_bot_YYYY-MM-DD.log)'
    )
    
    parser.add_argument(
        '--demo', '-d',
        action='store_true',
        help='Run in demo mode (no real API calls)'
    )
    
    parser.add_argument(
        '--auto-confirm', '-y',
        action='store_true',
        help='Skip confirmation prompt (useful for automation)'
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the CLI.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging(args.log_file)
    logger.info("Starting Trading Bot CLI")
    
    # Demo mode - no API keys needed
    if args.demo:
        logger.info("Running in DEMO mode (no real API calls)")
        print("\n" + "=" * 50)
        print("🎮 DEMO MODE")
        print("=" * 50)
        print("No real orders will be placed.")
        print("This simulates the API for testing purposes.")
        print("=" * 50)
        run_bot(args, demo_mode=True, logger=logger)
        return
    
    # Get API credentials from environment
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        logger.error("API credentials not found!")
        print("\nError: API credentials not found!")
        print("\nPlease set your Binance Futures Testnet API credentials:")
        print("1. Copy .env.example to .env")
        print("2. Add your API key and secret to the .env file")
        print("\nGet your API keys from: https://testnet.binancefuture.com")
        print("\nOr run in demo mode with --demo flag")
        sys.exit(1)
    
    run_bot(args, demo_mode=False, logger=logger, api_key=api_key, api_secret=api_secret)


def run_bot(args, demo_mode: bool, logger, api_key: str = None, api_secret: str = None):
    """
    Run the bot with the given arguments.
    
    Args:
        args: Parsed command line arguments
        demo_mode: Whether to use mock client
        logger: Logger instance
        api_key: API key (for real mode)
        api_secret: API secret (for real mode)
    """
    # Validate inputs
    is_valid, error_message = validate_all_inputs(
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price
    )
    
    if not is_valid:
        logger.error(f"Validation failed: {error_message}")
        print(f"\n❌ Error: {error_message}")
        sys.exit(1)
    
    logger.info("All inputs validated successfully")
    
    # Print order summary
    print("\n" + "-" * 50)
    print("ORDER SUMMARY")
    print("-" * 50)
    print(f"Symbol: {args.symbol.upper()}")
    print(f"Side: {args.side.upper()}")
    print(f"Type: {args.order_type.upper()}")
    print(f"Quantity: {args.quantity}")
    if args.price:
        print(f"Price: {args.price}")
    print("-" * 50)
    
    # Confirm order placement (unless auto-confirm)
    if not args.auto_confirm:
        confirm = input("\nDo you want to place this order? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("Order cancelled by user.")
            logger.info("Order cancelled by user")
            sys.exit(0)
    
    # Initialize client and order manager
    try:
        if demo_mode:
            client = MockBinanceClient()
            logger.info("Using MockBinanceClient (demo mode)")
        else:
            client = BinanceClient(api_key=api_key, api_secret=api_secret)
            logger.info("Using BinanceClient (real mode)")
        
        order_manager = OrderManager(client, logger)
        
        # Test connection (real mode only)
        if not demo_mode:
            logger.info("Testing API connection...")
            print("\nTesting API connection...")
            if not client.test_connection():
                logger.error("API connection test failed")
                print("\n❌ Error: Could not connect to Binance API. Please check your API credentials.")
                sys.exit(1)
            logger.info("API connection successful")
            print("✅ API connection successful")
        
    except Exception as e:
        logger.error(f"Failed to initialize client: {str(e)}")
        print(f"\n❌ Error: Failed to initialize client: {str(e)}")
        sys.exit(1)
    
    # Place the order
    try:
        print("\nPlacing order...")
        result = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=float(args.quantity),
            price=float(args.price) if args.price else None
        )
        
        # Print the result
        order_manager.print_order_summary(result)
        
        # Log completion
        if result['success']:
            logger.info(f"Order placed successfully. Order ID: {result['order_id']}")
            if demo_mode:
                print("\n⚠️  This was a DEMO order. No real transaction occurred.")
        else:
            logger.error(f"Order failed: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
