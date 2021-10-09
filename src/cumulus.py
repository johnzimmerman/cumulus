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

CBPRO_ENV = 'sandbox'

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
        print(f"printing response: {response}") #debug statement 
        return


if __name__ == "__main__":
    logging.info("Running Cumulus...")

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='name of the config file in ./conf/ directory', required=True)
    args = parser.parse_args()
    
    config_data = read_yaml("conf/sandbox.yml")
    api_url = config_data["cbpro"]["url"]
    key = config_data["cbpro"]["key"]
    secret = config_data["cbpro"]["secret"]
    passphrase = config_data["cbpro"]["passphrase"]
    order_form = config_data["order_form"]

    auth_client = cbpro.AuthenticatedClient(
        key, secret, passphrase, api_url=api_url)
    my_order_manager = OrderManager(auth_client)

    for order in order_form:
        asset = order["asset"]
        amount = order["amount"]
        my_order_manager.placeMarketOrder(asset, amount)
