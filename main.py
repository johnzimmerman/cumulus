#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cumulus.py: Dollar-cost average cryptocurrency on Coinbase Pro."""

import logging
from os import environ

import cbpro
from flask import escape


# Set logging format
# e.g. 2021-06-20 12:09:10,767 - INFO - Running cumulus.py
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

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
        logging.info(f"Attempting to purchase ${amount} of {product_id}.")
        response = self.client.place_market_order(
            product_id=product_id,
            side='buy',
            funds=amount)
        if "message" in response:
            logging.warning(response["message"])
        else:
            logging.info(
                f"Your purchase for ${amount} of {product_id} has started.")
        return


def cumulus_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    # if request_json and 'name' in request_json:
    #     name = request_json['name']
    # elif request_args and 'name' in request_args:
    #     name = request_args['name']
    # else:
    #     name = 'World'
    # return 'Hello {}!'.format(escape(name))

    logging.info("Running Cumulus...")
    auth_client = cbpro.AuthenticatedClient(
        API_KEY, API_SECRET, API_PASSPHRASE,
        api_url=API_URL)
    my_order_manager = OrderManager(auth_client)
    my_order_manager.placeMarketOrder("BTC-USD", 15.00)
    return "OK"
