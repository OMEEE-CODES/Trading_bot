"""
Input validation functions for the trading bot.

This module contains functions to validate user inputs before 
sending them to the Binance API.
"""

import re
from typing import Tuple, Optional


def validate_symbol(symbol: str) -> Tuple[bool, Optional[str]]:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading pair (e.g., BTCUSDT)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not symbol:
        return False, "Symbol cannot be empty"
    
    # Symbol should be uppercase letters/numbers (e.g., BTCUSDT, ETHUSDT)
    if not re.match(r'^[A-Z0-9]+$', symbol):
        return False, f"Invalid symbol format: '{symbol}'. Use uppercase letters only (e.g., BTCUSDT)"
    
    # Common symbols are at least 6 characters (e.g., BTCUSDT)
    if len(symbol) < 6:
        return False, f"Symbol '{symbol}' seems too short"
    
    return True, None


def validate_side(side: str) -> Tuple[bool, Optional[str]]:
    """
    Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not side:
        return False, "Side cannot be empty"
    
    side = side.upper()
    valid_sides = ["BUY", "SELL"]
    
    if side not in valid_sides:
        return False, f"Invalid side: '{side}'. Must be one of: {', '.join(valid_sides)}"
    
    return True, None


def validate_order_type(order_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate order type.
    
    Args:
        order_type: Order type (MARKET or LIMIT)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not order_type:
        return False, "Order type cannot be empty"
    
    order_type = order_type.upper()
    valid_types = ["MARKET", "LIMIT"]
    
    if order_type not in valid_types:
        return False, f"Invalid order type: '{order_type}'. Must be one of: {', '.join(valid_types)}"
    
    return True, None


def validate_quantity(quantity: str) -> Tuple[bool, Optional[str]]:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity as string
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not quantity:
        return False, "Quantity cannot be empty"
    
    try:
        qty = float(quantity)
        if qty <= 0:
            return False, f"Quantity must be positive, got: {qty}"
        return True, None
    except ValueError:
        return False, f"Invalid quantity: '{quantity}'. Must be a number"


def validate_price(price: str, order_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate order price.
    
    Args:
        price: Order price as string
        order_type: Type of order (price required for LIMIT)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    order_type = order_type.upper()
    
    # Price is required for LIMIT orders
    if order_type == "LIMIT":
        if not price:
            return False, "Price is required for LIMIT orders"
        
        try:
            p = float(price)
            if p <= 0:
                return False, f"Price must be positive, got: {p}"
            return True, None
        except ValueError:
            return False, f"Invalid price: '{price}'. Must be a number"
    
    # Price should not be provided for MARKET orders
    if order_type == "MARKET" and price:
        return False, "Price should not be provided for MARKET orders (price is determined by market)"
    
    return True, None


def validate_all_inputs(symbol: str, side: str, order_type: str, 
                        quantity: str, price: str = None) -> Tuple[bool, str]:
    """
    Validate all order inputs.
    
    Args:
        symbol: Trading pair
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Order price (required for LIMIT)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    validators = [
        validate_symbol(symbol),
        validate_side(side),
        validate_order_type(order_type),
        validate_quantity(quantity),
        validate_price(price, order_type)
    ]
    
    for is_valid, error_message in validators:
        if not is_valid:
            return False, error_message
    
    return True, "All inputs are valid"
