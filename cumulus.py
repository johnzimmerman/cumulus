#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cumulus.py: Dollar-cost average cryptocurrency with the Coinbase Advanced Trade API."""

import hashlib
import hmac
import json
import logging
import os
import time
import uuid

import requests
import yaml


# Set config file constants
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(THIS_DIR, 'config.yml')

# Set logging format
# e.g. 2021-06-20 12:09:10,767 - INFO - Running cumulus.py
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def read_config_file(file_path):
    """
    Reads and parses a configuration file in YAML format from the specified file path.

    Args:
        file_path (str): The path to the configuration file to be read.

    Returns:
        dict or None: If successful, returns a dictionary containing the configuration data.
                     If any errors occur, returns None.

    Raises:
        FileNotFoundError: If the specified file does not exist at the provided file_path.
        yaml.
        YAMLError: If there is an issue parsing the YAML content of the file.
        Exception: For any other unexpected errors during file reading.
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file at path '{file_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class CoinbaseAdvancedTradeAuth(requests.auth.AuthBase):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url.split('?')[0] + str(request.body or '')
        signature = hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        request.headers.update({
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-SIGN': signature,
            'CB-VERSION': '2023-07-15',
            'Content-Type': 'application/json'
        })

        return request


def place_order(auth, product_id, amount):
    """
    Place a market order for the given product ID and amount.

    Args:
        auth (CoinbaseAdvancedTradeAuth): The authentication object.
        product_id (str): The product ID. (e.g. 'BTC-USD')
        amount (float): The amount of the order.

    Returns:
        requests.Response: The response from the API.
    """
    url = 'https://api.coinbase.com/api/v3/brokerage/orders'
    data = {
        'product_id': product_id,
        'side': "BUY",
        'order_configuration': {
            'market_market_ioc': { 'quote_size': str(amount) }
        },
        'client_order_id': str(uuid.uuid4())
    }
    # Serialize the data object to JSON so that it can be read in request.body
    json_data = json.dumps(data)

    try:
        response = requests.post(url, auth=auth, data=json_data)
        if response.status_code == 200:
            if response.json()['success'] == True:
                logging.info(f"Purchased {amount} of {product_id} successfully.")
            else:
                logging.error(f"Purchase of {amount} of {product_id} failed. Response: {response.json()['error_response']['message']}")
        else:
            logging.error(f"Purchase of {amount} of {product_id} failed. Response: {response.json()['message']}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Purchase of {amount} of {product_id} failed: {str(e)}")
    return 


if __name__ == "__main__":
    logging.info("Running Cumulus Advanced Trade.")
    try:
        config_data = read_config_file(CONFIG_FILE)
        if config_data:
            api_key = config_data["coinbase_api"]["key"]
            api_secret = config_data["coinbase_api"]["secret"]
            order_form = config_data ["order_form"]

            cb_auth = CoinbaseAdvancedTradeAuth(api_key, api_secret)

            for order in order_form:
                place_order(cb_auth, order['product'], order['amount'])
        else:
            logging.error("Config data is empty or could not be read.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    logging.info("Cumulus Advanced Trade finished running.")