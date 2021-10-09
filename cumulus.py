#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cumulus.py: Dollar-cost average cryptocurrency on Coinbase Pro."""

import argparse
import logging

import cbpro
import yaml

# Set logging format
# e.g. 2021-06-20 12:09:10,767 - INFO - Running cumulus.py
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class OrderManager:
    """Manage your orders."""

    def __init__(self, cbpro_auth_client):
        self.client = cbpro_auth_client

    def placeMarketOrder(self, product_id, amount):
        logging.info(f"Attempting order: {product_id} ${amount}")
        response = self.client.place_market_order(
            product_id=product_id,
            side='buy',
            funds=amount)
        if "message" in response:
            logging.warning(response["message"])
        else:
            logging.info(
                f"Placed order: {product_id} ${amount}")
        print(f"printing response: {response}")  # debug statement
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--production', action='store_const', const='production', default='sandbox',
                        help='use coinbase pro production env')
    args = parser.parse_args()
    
    ENVIRONMENT = args.production
    URL = 'https://api.exchange.coinbase.com' if ENVIRONMENT == 'production' else 'https://api-public.sandbox.exchange.coinbase.com'

    logging.info("Running Cumulus...")
    # TODO: Gracefully exit if file isn't found
    config_data = read_yaml("config.yml")

    KEY = config_data[ENVIRONMENT]["cbpro"]["key"]
    SECRET = config_data[ENVIRONMENT]["cbpro"]["secret"]
    PASSPHRASE = config_data[ENVIRONMENT]["cbpro"]["passphrase"]
    ORDER_FORM = config_data[ENVIRONMENT]["order_form"]

    auth_client = cbpro.AuthenticatedClient(
        KEY, SECRET, PASSPHRASE, api_url=URL)
    my_order_manager = OrderManager(auth_client)

    for order in ORDER_FORM:
        asset = order["asset"]
        amount = order["amount"]
        my_order_manager.placeMarketOrder(asset, amount)
