"""
Binance Futures Testnet API Client.

This module provides a simple wrapper around the Binance Futures Testnet API
for placing orders and handling authentication.
"""

import hmac
import hashlib
import time
from typing import Dict, Optional, Any
import requests


class BinanceClient:
    """
    Client for interacting with Binance Futures Testnet API.
    
    Attributes:
        api_key: Binance API key
        api_secret: Binance API secret
        base_url: Base URL for the API
    """
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Binance client.
        
        Args:
            api_key: Your Binance API key
            api_secret: Your Binance API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"
    
    def _generate_signature(self, query_string: str) -> str:
        """
        Generate HMAC SHA256 signature for API authentication.
        
        Args:
            query_string: Query string to sign
        
        Returns:
            Hexadecimal signature string
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers required for API requests.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def _make_request(self, method: str, endpoint: str, 
                      params: Dict[str, Any] = None) -> Dict:
        """
        Make an authenticated request to the Binance API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint (e.g., /fapi/v1/order)
            params: Request parameters
        
        Returns:
            JSON response from the API
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if params is None:
            params = {}
        
        # Add timestamp for authentication
        params['timestamp'] = int(time.time() * 1000)
        
        # Create query string and signature
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"
        
        # Construct full URL
        url = f"{self.base_url}{endpoint}?{query_string}"
        
        # Make request
        if method == "POST":
            response = requests.post(url, headers=self._get_headers())
        elif method == "GET":
            response = requests.get(url, headers=self._get_headers())
        elif method == "DELETE":
            response = requests.delete(url, headers=self._get_headers())
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Check for errors
        response.raise_for_status()
        
        return response.json()
    
    def place_order(self, symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None) -> Dict:
        """
        Place a new order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
        
        Returns:
            Order response from the API
        """
        # Build order parameters
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }
        
        # Add price for LIMIT orders
        if order_type.upper() == "LIMIT":
            params['price'] = price
            params['timeInForce'] = 'GTC'  # Good Till Cancelled
        
        return self._make_request("POST", "/fapi/v1/order", params)
    
    def test_connection(self) -> bool:
        """
        Test if API credentials are working.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to get account information
            params = {'timestamp': int(time.time() * 1000)}
            query_string = f"timestamp={params['timestamp']}"
            signature = self._generate_signature(query_string)
            url = f"{self.base_url}/fapi/v1/account?{query_string}&signature={signature}"
            
            response = requests.get(url, headers=self._get_headers())
            return response.status_code == 200
        except Exception:
            return False


class MockBinanceClient:
    """
    Mock client for demonstration/testing without real API keys.
    
    This simulates the Binance API responses for testing purposes.
    """
    
    def __init__(self, api_key: str = "demo", api_secret: str = "demo"):
        """Initialize mock client."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com (MOCK)"
        self._order_counter = 123456789
    
    def test_connection(self) -> bool:
        """Always returns True for demo mode."""
        return True
    
    def place_order(self, symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None) -> dict:
        """
        Simulate placing an order.
        
        Returns a realistic-looking order response.
        """
        import time
        
        self._order_counter += 1
        current_time = int(time.time() * 1000)
        
        # Simulate market price for realistic avgPrice
        mock_market_price = 43250.50
        
        response = {
            "orderId": self._order_counter,
            "symbol": symbol.upper(),
            "status": "FILLED" if order_type.upper() == "MARKET" else "NEW",
            "clientOrderId": f"demo_{self._order_counter}",
            "price": str(price) if price else "0.00",
            "avgPrice": str(mock_market_price) if order_type.upper() == "MARKET" else "0.0000",
            "origQty": str(quantity),
            "executedQty": str(quantity) if order_type.upper() == "MARKET" else "0.000",
            "cumQuote": str(float(quantity) * mock_market_price) if order_type.upper() == "MARKET" else "0.0000",
            "timeInForce": "GTC" if order_type.upper() == "LIMIT" else "GTC",
            "type": order_type.upper(),
            "side": side.upper(),
            "time": current_time,
            "updateTime": current_time,
            "workingType": "CONTRACT_PRICE",
            "priceProtect": False
        }
        
        return response
