"""
Logging configuration for the trading bot.

This module sets up logging to both console and file.
"""

import logging
import sys
from datetime import datetime


def setup_logging(log_file: str = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_file: Path to log file. If None, uses 'trading_bot_YYYY-MM-DD.log'
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    # Console handler (simple output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler (detailed output)
    if log_file is None:
        log_file = f"trading_bot_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger
