#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cumulus.py: Dollar-cost average cryptocurrency on Coinbase Pro."""

import logging
from os import environ

import cbpro


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# TODO: If the variables are in the ENV but empty, no warning is given
# https://www.twilio.com/blog/environment-variables-python
API_URL = environ.get(
    "CBPRO_API_URL") or "https://api-public.sandbox.pro.coinbase.com"
API_KEY = environ["CBPRO_KEY"]
API_SECRET = environ["CBPRO_SECRET"]
API_PASSPHRASE = environ["CBPRO_PASSPHRASE"]


class OrderManager:
    """Manage your orders."""

    def __init__(self, cbpro_auth_client):
        self.client = cbpro_auth_client

    def placeMarketOrder(self, product_id, amount):
        logging.info(f"Attempting to purchase {amount} of {product_id}.")
        # TODO: Ensure amount is correctly formatted
        response = self.client.place_market_order(
            product_id=product_id,
            side='buy',
            funds=amount)
        print(response)


if __name__ == "__main__":
    logging.info("Running cumulus.py")
    auth_client = cbpro.AuthenticatedClient(
        API_KEY, API_SECRET, API_PASSPHRASE,
        api_url=API_URL)
    # accounts = auth_client.get_accounts()
    # print(accounts)
    my_order_manager = OrderManager(auth_client)
    my_order_manager.placeMarketOrder("BTC-USD", "100.00")
