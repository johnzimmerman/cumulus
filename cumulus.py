#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A trading bot that executes cryptocurrency purchases on Coinbase Advanced using their API.
Reads trading configuration from trading_plan.yml and executes orders accordingly.
"""

# Standard library imports
import argparse
import logging
import os
import sys
import time

# Third-party imports
from coinbase.rest import RESTClient
import yaml

# Configure logging to stdout
def setup_logging() -> logging.Logger:
    logger = logging.getLogger('cumulus2')
    logger.setLevel(logging.INFO)
    
    # Create formatter and handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger


class TradingPlanLoader:
    """Class to load and validate the trading plan from a YAML file."""
    
    def __init__(self):
        self.orders = self._load_trading_plan()  # Load and validate the trading plan

    def _load_trading_plan(self):
        try:
            with open('trading_plan.yml', 'r') as file:
                trading_plan = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                "trading_plan.yml not found. Please create this file from trading_plan.yml.template "
                "and specify your desired trade amounts."
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing trading_plan.yml: {str(e)}")
        
        if 'trades' not in trading_plan or not trading_plan['trades']:
            raise ValueError("Trading plan must contain a 'trades' section and cannot be empty.")
        
        # Convert the simple format into order information
        orders = []
        for crypto, amount in trading_plan['trades'].items():
            amount_usd = float(amount.replace('$', ''))
            orders.append({
                'product': f"{crypto}-USD",
                'amount': amount_usd
            })

        if not orders:
            raise ValueError("No valid trades found in trading plan")

        return orders # Return the list of orders


class CoinbaseClient:
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    def __init__(self, logger: logging.Logger, is_production_mode: bool = False):
        key_path = "secrets/cdp_api_key.json"
        
        if not os.path.exists(key_path):
            raise FileNotFoundError(
                f"Coinbase API key file not found at {key_path}. "
                "Please download your API key file from Coinbase and place it in the secrets directory."
            )
            
        base_url = "api-sandbox.coinbase.com" if not is_production_mode else "api.coinbase.com"
        
        try:
            self.client = RESTClient(
                key_file=key_path,
                base_url=base_url
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Coinbase client: {str(e)}")
            
        self.logger = logger
    
    def place_market_order(self, product_id: str, amount_usd: float) -> bool:
        """
        Places a market buy order with retry logic.
        Returns True if successful, False otherwise.
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                # Place market order using market_order_buy
                order = self.client.market_order_buy(
                    client_order_id="",  # Empty string will auto-generate a unique ID
                    product_id=product_id,
                    quote_size=str(amount_usd)
                )
                
                # Log successful order
                self.logger.info(
                    f"Successfully placed order - Product: {product_id}, "
                    f"Amount: ${amount_usd:.2f}, "
                    f"Transaction ID: {order['order_id']}, "
                    f"Status: {order['status']}"
                )
                return True
                
            except Exception as e:
                self.logger.warning(
                    f"Attempt {attempt + 1}/{self.MAX_RETRIES} failed for {product_id}: {str(e)}"
                )
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                else:
                    self.logger.error(
                        f"Failed to place order after {self.MAX_RETRIES} attempts - "
                        f"Product: {product_id}, Amount: ${amount_usd:.2f}"
                    )
                    return False

def main():
    logger = setup_logging()
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run the trading bot.")
    parser.add_argument('--production', '-p', action='store_true', help='Run in production mode')
    args = parser.parse_args()

    # Determine if we are in production mode
    is_production_mode = args.production

    # Log the mode
    logger.info(f"Running in {'production' if is_production_mode else 'sandbox'} mode")

    try:
        # Load trading plan
        trading_plan = TradingPlanLoader() # No arguments needed
        orders = trading_plan.orders # Get the list of orders
        
        # Initialize Coinbase client
        client = CoinbaseClient(
            logger=logger,
            is_production_mode=is_production_mode # Set production mode based on argument
        )
        
        # Process each order
        for order in orders:
            product_id = order['product']
            amount = float(order['amount'])
            
            logger.info(f"Processing order for {product_id} - Amount: ${amount:.2f}")
            client.place_market_order(product_id, amount)
            
        logger.info("Order processing completed")
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
