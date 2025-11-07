#!/usr/bin/env python3
"""
Automated Trading Bot with Stop Loss and Take Profit

This bot:
1. Identifies the most traded stock in the US market
2. Buys with the available pot amount
3. Sets a 10% stop loss
4. Sets a 10% take profit
5. Continues trading until target profit is reached

Author: Automated Trading System
License: MIT
"""

import alpaca_trade_api as tradeapi
import time
import logging
from datetime import datetime
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, config):
        self.config = config
        self.api = tradeapi.REST(
            config.API_KEY,
            config.API_SECRET,
            config.BASE_URL,
            api_version='v2'
        )
        self.pot = config.INITIAL_POT
        self.total_profit = 0.0
        self.trades_completed = 0
        
        logger.info(f"Trading Bot initialized with pot: ${self.pot}")
        logger.info(f"Target profit: ${config.PROFIT_TARGET}")
    
    def get_most_traded_stock(self):
        """
        Find the most traded stock by volume in the US market.
        Returns the stock symbol.
        """
        try:
            logger.info("Searching for most traded stock...")
            
            # Get active US stocks
            assets = self.api.list_assets(status='active', asset_class='us_equity')
            
            max_volume = 0
            top_symbol = None
            
            # Check top tradable stocks
            for asset in assets[:100]:  # Check top 100 for efficiency
                if not asset.tradable or not asset.shortable:
                    continue
                
                try:
                    # Get latest bar data
                    barset = self.api.get_barset(asset.symbol, 'day', limit=1)
                    if asset.symbol in barset:
                        volume = barset[asset.symbol][0].v
                        if volume > max_volume:
                            max_volume = volume
                            top_symbol = asset.symbol
                except Exception as e:
                    continue
            
            logger.info(f"Most traded stock: {top_symbol} with volume: {max_volume}")
            return top_symbol
            
        except Exception as e:
            logger.error(f"Error finding most traded stock: {e}")
            return None
    
    def get_current_price(self, symbol):
        """
        Get the current market price for a symbol.
        """
        try:
            trade = self.api.get_latest_trade(symbol)
            return float(trade.price)
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return None
    
    def place_buy_order(self, symbol, quantity):
        """
        Place a market buy order.
        """
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='day'
            )
            logger.info(f"Buy order placed: {quantity} shares of {symbol}")
            return order
        except Exception as e:
            logger.error(f"Error placing buy order: {e}")
            return None
    
    def place_sell_order(self, symbol, quantity):
        """
        Place a market sell order.
        """
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='day'
            )
            logger.info(f"Sell order placed: {quantity} shares of {symbol}")
            return order
        except Exception as e:
            logger.error(f"Error placing sell order: {e}")
            return None
    
    def monitor_position(self, symbol, entry_price, quantity, stop_loss_price, take_profit_price):
        """
        Monitor the position and sell when stop loss or take profit is hit.
        """
        logger.info(f"Monitoring position: {symbol}")
        logger.info(f"Entry: ${entry_price:.2f}, Stop Loss: ${stop_loss_price:.2f}, Take Profit: ${take_profit_price:.2f}")
        
        while True:
            try:
                current_price = self.get_current_price(symbol)
                
                if current_price is None:
                    time.sleep(self.config.CHECK_INTERVAL)
                    continue
                
                # Check stop loss
                if current_price <= stop_loss_price:
                    logger.warning(f"Stop loss triggered at ${current_price:.2f}")
                    self.place_sell_order(symbol, quantity)
                    loss = (current_price - entry_price) * quantity
                    return loss, 'stop_loss'
                
                # Check take profit
                elif current_price >= take_profit_price:
                    logger.info(f"Take profit triggered at ${current_price:.2f}")
                    self.place_sell_order(symbol, quantity)
                    profit = (current_price - entry_price) * quantity
                    return profit, 'take_profit'
                
                time.sleep(self.config.CHECK_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error monitoring position: {e}")
                time.sleep(self.config.CHECK_INTERVAL)
    
    def execute_trade_cycle(self):
        """
        Execute one complete trade cycle.
        """
        logger.info(f"\n{'='*50}")
        logger.info(f"Starting trade cycle #{self.trades_completed + 1}")
        logger.info(f"Current pot: ${self.pot:.2f}")
        logger.info(f"Total profit so far: ${self.total_profit:.2f}")
        logger.info(f"{'='*50}\n")
        
        # Find most traded stock
        symbol = self.get_most_traded_stock()
        if not symbol:
            logger.error("Could not find suitable stock to trade")
            return False
        
        # Get current price
        entry_price = self.get_current_price(symbol)
        if not entry_price:
            logger.error(f"Could not get price for {symbol}")
            return False
        
        # Calculate quantity to buy
        quantity = int(self.pot / entry_price)
        if quantity == 0:
            logger.error(f"Insufficient funds to buy {symbol} at ${entry_price:.2f}")
            return False
        
        # Calculate stop loss and take profit prices
        stop_loss_price = entry_price * (1 - self.config.STOP_LOSS_PCT)
        take_profit_price = entry_price * (1 + self.config.TAKE_PROFIT_PCT)
        
        logger.info(f"Trading {symbol}:")
        logger.info(f"  Quantity: {quantity}")
        logger.info(f"  Entry price: ${entry_price:.2f}")
        logger.info(f"  Stop loss: ${stop_loss_price:.2f} (-{self.config.STOP_LOSS_PCT*100}%)")
        logger.info(f"  Take profit: ${take_profit_price:.2f} (+{self.config.TAKE_PROFIT_PCT*100}%)")
        
        # Place buy order
        buy_order = self.place_buy_order(symbol, quantity)
        if not buy_order:
            return False
        
        # Wait for order to fill
        time.sleep(5)
        
        # Monitor position
        result, exit_type = self.monitor_position(
            symbol, entry_price, quantity, stop_loss_price, take_profit_price
        )
        
        # Update pot and profit
        self.pot += result
        self.total_profit += result
        self.trades_completed += 1
        
        logger.info(f"\nTrade completed via {exit_type}")
        logger.info(f"Result: ${result:.2f}")
        logger.info(f"New pot: ${self.pot:.2f}")
        logger.info(f"Total profit: ${self.total_profit:.2f}")
        
        return True
    
    def run(self):
        """
        Main bot loop - runs until profit target is reached.
        """
        logger.info("\n" + "="*60)
        logger.info("TRADING BOT STARTED")
        logger.info(f"Initial Pot: ${self.pot:.2f}")
        logger.info(f"Profit Target: ${self.config.PROFIT_TARGET:.2f}")
        logger.info(f"Stop Loss: {self.config.STOP_LOSS_PCT*100}%")
        logger.info(f"Take Profit: {self.config.TAKE_PROFIT_PCT*100}%")
        logger.info("="*60 + "\n")
        
        while self.total_profit < self.config.PROFIT_TARGET:
            try:
                success = self.execute_trade_cycle()
                
                if not success:
                    logger.warning("Trade cycle failed, waiting before retry...")
                    time.sleep(60)
                    continue
                
                # Check if target reached
                if self.total_profit >= self.config.PROFIT_TARGET:
                    logger.info("\n" + "="*60)
                    logger.info("🎉 PROFIT TARGET REACHED! 🎉")
                    logger.info(f"Total profit: ${self.total_profit:.2f}")
                    logger.info(f"Final pot: ${self.pot:.2f}")
                    logger.info(f"Trades completed: {self.trades_completed}")
                    logger.info("="*60 + "\n")
                    break
                
                # Wait before next trade
                time.sleep(self.config.TRADE_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("\nBot stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    # Load configuration
    config = Config()
    
    # Create and run bot
    bot = TradingBot(config)
    bot.run()
