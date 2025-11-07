#!/usr/bin/env python3
"""
Configuration File for Automated Trading Bot

Stores all configurable parameters including:
- API credentials
- Trading parameters (pot size, profit targets, stop loss, take profit)
- Timing intervals
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the trading bot.
    All parameters can be modified here or via environment variables.
    """
    
    # ============ API CREDENTIALS ============
    # Get these from your Alpaca account: https://alpaca.markets/
    # For paper trading (recommended for testing): https://paper-api.alpaca.markets
    # For live trading: https://api.alpaca.markets
    
    API_KEY = os.getenv('ALPACA_API_KEY', 'YOUR_ALPACA_API_KEY_HERE')
    API_SECRET = os.getenv('ALPACA_API_SECRET', 'YOUR_ALPACA_SECRET_KEY_HERE')
    BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')  # Paper trading by default
    
    # ============ TRADING PARAMETERS ============
    
    # Initial capital to start trading with (in USD)
    INITIAL_POT = float(os.getenv('INITIAL_POT', 1000.0))
    
    # Target profit before stopping the bot (in USD)
    PROFIT_TARGET = float(os.getenv('PROFIT_TARGET', 500.0))
    
    # Stop loss percentage (0.10 = 10%)
    STOP_LOSS_PCT = float(os.getenv('STOP_LOSS_PCT', 0.10))
    
    # Take profit percentage (0.10 = 10%)
    TAKE_PROFIT_PCT = float(os.getenv('TAKE_PROFIT_PCT', 0.10))
    
    # ============ TIMING PARAMETERS ============
    
    # How often to check price for stop loss / take profit (in seconds)
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 30))  # Check every 30 seconds
    
    # Wait time between trades (in seconds)
    TRADE_INTERVAL = int(os.getenv('TRADE_INTERVAL', 60))  # Wait 1 minute between trades
    
    # ============ RISK MANAGEMENT ============
    
    # Maximum number of consecutive losses before pausing
    MAX_CONSECUTIVE_LOSSES = int(os.getenv('MAX_CONSECUTIVE_LOSSES', 3))
    
    # Minimum stock price to consider (avoid penny stocks)
    MIN_STOCK_PRICE = float(os.getenv('MIN_STOCK_PRICE', 5.0))
    
    # Maximum stock price to consider (control position size)
    MAX_STOCK_PRICE = float(os.getenv('MAX_STOCK_PRICE', 500.0))
    
    # ============ LOGGING ============
    
    # Log file path
    LOG_FILE = os.getenv('LOG_FILE', 'trading_bot.log')
    
    # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    def __init__(self):
        """
        Initialize and validate configuration.
        """
        self.validate()
    
    def validate(self):
        """
        Validate configuration parameters.
        Raises ValueError if any parameter is invalid.
        """
        if self.API_KEY == 'YOUR_ALPACA_API_KEY_HERE':
            raise ValueError(
                "Please set your Alpaca API key in config.py or as environment variable ALPACA_API_KEY"
            )
        
        if self.API_SECRET == 'YOUR_ALPACA_SECRET_KEY_HERE':
            raise ValueError(
                "Please set your Alpaca API secret in config.py or as environment variable ALPACA_API_SECRET"
            )
        
        if self.INITIAL_POT <= 0:
            raise ValueError("Initial pot must be greater than 0")
        
        if self.PROFIT_TARGET <= 0:
            raise ValueError("Profit target must be greater than 0")
        
        if not (0 < self.STOP_LOSS_PCT < 1):
            raise ValueError("Stop loss percentage must be between 0 and 1")
        
        if not (0 < self.TAKE_PROFIT_PCT < 1):
            raise ValueError("Take profit percentage must be between 0 and 1")
        
        if self.CHECK_INTERVAL <= 0:
            raise ValueError("Check interval must be greater than 0")
    
    def display(self):
        """
        Display current configuration (without sensitive data).
        """
        print("\n" + "="*60)
        print("TRADING BOT CONFIGURATION")
        print("="*60)
        print(f"Base URL: {self.BASE_URL}")
        print(f"Initial Pot: ${self.INITIAL_POT:.2f}")
        print(f"Profit Target: ${self.PROFIT_TARGET:.2f}")
        print(f"Stop Loss: {self.STOP_LOSS_PCT*100}%")
        print(f"Take Profit: {self.TAKE_PROFIT_PCT*100}%")
        print(f"Check Interval: {self.CHECK_INTERVAL}s")
        print(f"Trade Interval: {self.TRADE_INTERVAL}s")
        print(f"Max Consecutive Losses: {self.MAX_CONSECUTIVE_LOSSES}")
        print(f"Stock Price Range: ${self.MIN_STOCK_PRICE:.2f} - ${self.MAX_STOCK_PRICE:.2f}")
        print("="*60 + "\n")

if __name__ == "__main__":
    # Test configuration
    try:
        config = Config()
        config.display()
        print("✅ Configuration is valid!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
