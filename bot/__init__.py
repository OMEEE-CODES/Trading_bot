"""
Trading Bot package for Binance Futures Testnet.

This package provides a simple interface to place orders on 
Binance Futures Testnet (USDT-M).
"""

from .client import BinanceClient
from .orders import OrderManager

__all__ = ["BinanceClient", "OrderManager"]
