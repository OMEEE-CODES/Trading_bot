"""
Order management module for the trading bot.

This module handles order placement and response formatting.
"""

from typing import Dict, Any
import logging

from .client import BinanceClient


class OrderManager:
    """
    Manages order placement and response handling.
    
    This class provides a higher-level interface for placing orders
    and formatting the results.
    
    Attributes:
        client: BinanceClient instance for API calls
        logger: Logger instance for logging
    """
    
    def __init__(self, client: BinanceClient, logger: logging.Logger = None):
        """
        Initialize the OrderManager.
        
        Args:
            client: BinanceClient instance
            logger: Optional logger instance
        """
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def place_order(self, symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None) -> Dict[str, Any]:
        """
        Place an order and return formatted result.
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
        
        Returns:
            Dictionary containing order result and metadata
        """
        # Log the order request
        self.logger.info(f"Placing {order_type} {side} order: {quantity} {symbol}")
        if price:
            self.logger.info(f"Limit price: {price}")
        
        try:
            # Place the order
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
            
            # Log the response
            self.logger.debug(f"API Response: {response}")
            
            # Format and return the result
            return self._format_success_response(response)
            
        except Exception as e:
            self.logger.error(f"Order failed: {str(e)}")
            return self._format_error_response(str(e))
    
    def _format_success_response(self, response: Dict) -> Dict[str, Any]:
        """
        Format a successful order response.
        
        Args:
            response: Raw API response
        
        Returns:
            Formatted response dictionary
        """
        return {
            'success': True,
            'order_id': response.get('orderId'),
            'symbol': response.get('symbol'),
            'side': response.get('side'),
            'type': response.get('type'),
            'status': response.get('status'),
            'quantity': response.get('origQty'),
            'executed_quantity': response.get('executedQty'),
            'average_price': response.get('avgPrice', 'N/A'),
            'price': response.get('price'),
            'created_time': response.get('time'),
            'raw_response': response
        }
    
    def _format_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        Format an error response.
        
        Args:
            error_message: Error message string
        
        Returns:
            Formatted error dictionary
        """
        return {
            'success': False,
            'error': error_message
        }
    
    def print_order_summary(self, result: Dict[str, Any]) -> None:
        """
        Print a formatted order summary to the console.
        
        Args:
            result: Order result dictionary
        """
        print("\n" + "=" * 50)
        print("ORDER RESULT")
        print("=" * 50)
        
        if result['success']:
            print(f"Status: {'SUCCESS' if result['status'] in ['NEW', 'FILLED', 'PARTIALLY_FILLED'] else result['status']}")
            print(f"Order ID: {result['order_id']}")
            print(f"Symbol: {result['symbol']}")
            print(f"Side: {result['side']}")
            print(f"Type: {result['type']}")
            print(f"Quantity: {result['quantity']}")
            
            if result['price'] and result['type'] == 'LIMIT':
                print(f"Limit Price: {result['price']}")
            
            print(f"Executed Qty: {result['executed_quantity']}")
            
            if result['average_price'] and result['average_price'] != '0.0000':
                print(f"Average Price: {result['average_price']}")
            
            print(f"Order Status: {result['status']}")
        else:
            print(f"Status: FAILED")
            print(f"Error: {result['error']}")
        
        print("=" * 50 + "\n")
