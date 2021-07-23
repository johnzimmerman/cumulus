#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cumulus.py: Dollar-cost average cryptocurrency on Coinbase Pro."""

import logging
from os import environ

from proto import message

import cbpro
from flask import escape
from google.cloud import secretmanager
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# Set logging format
# e.g. 2021-06-20 12:09:10,767 - INFO - Running Cumulus...
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

# TODO: If the variables are in the ENV but empty, no warning is given
# https://www.twilio.com/blog/environment-variables-python
API_URL = environ.get(
    "CBPRO_API_URL") or "https://api-public.sandbox.pro.coinbase.com"
try:
    PROJECT_ID = environ["PROJECT_ID"]
except KeyError:
    logging.error("Unable to find GCP Project ID.")
API_KEY = access_secret_version(PROJECT_ID, "SANDBOX_CBPRO_KEY", "latest")
API_SECRET = access_secret_version(
    PROJECT_ID, "SANDBOX_CBPRO_SECRET", "latest")
API_PASSPHRASE = access_secret_version(
    PROJECT_ID, "SANDBOX_CBPRO_PASSPHRASE", "latest")


def sendEmail(to_email):
    message = Mail(
        from_email="jfzimmerman@gmail.com",
        to_emails=to_email,
        subject="Your Coinbase Pro Trade(s)",
        html_content="<strong>and easy to do anywhere, even with Python</strong>")
    try:
        sg = SendGridAPIClient(environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


class OrderManager:
    """Manage your orders."""

    def __init__(self, cbpro_auth_client):
        self.client = cbpro_auth_client
        self.placed_orders = []
        self.order_errors = []
        logging.info("Initialized OrderManager.")

    def getOrder(self, id):
        try:
            response = self.client.get_order(id)
            # The "message" attribute will only appear in an error situation.
            if "message" in response:
                logging.warning(
                    f"Failed to get order ID: {id} - {response['message']}.")
            else:
                logging.info(f"Retrieved order ID: {id}.")
        except Exception as e:
            logging.warning(e.message)

        return response

    def placeMarketOrder(self, product_id, amount):
        try:
            logging.info(f"Attempting to purchase ${amount} of {product_id}.")

            response = self.client.place_market_order(
                product_id=product_id,
                side='buy',
                funds=amount)

            # The "message" attribute will only appear in an error situation.
            if "message" in response:
                logging.warning(f"PURCHASE FAILED - {response['message']}.")

                # Add error to data structure for email.
                self.order_errors.append(
                    {
                        "product_id": product_id,
                        "amount": amount,
                        "message": response["message"]
                    }
                )
            else:
                logging.info(
                    f"Your purchase for ${amount} of {product_id} has started.")
                # Add order info to use later. fill_fees, filled_size, and
                # executed_value will be 0 at this stage. status should be
                # in pending and settled should be false. This info will
                # be updated later before sending the email receipt.
                self.placed_orders.append(response)
        except Exception as e:
            logging.warning(e.message)

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
    logging.info("Running Cumulus...")

    request_json = request.get_json(silent=True)
    # print(request_json)
    if request_json and "buy_orders" in request_json:
        buy_orders = request_json["buy_orders"]

        auth_client = cbpro.AuthenticatedClient(
            API_KEY, API_SECRET, API_PASSPHRASE,
            api_url=API_URL)

        my_order_manager = OrderManager(auth_client)

        # Place the orders via OrderManager.
        for order in buy_orders:
            product = order["product"]
            amount = order["amount"]
            my_order_manager.placeMarketOrder(product, amount)

        # Attempt to get settled order info.
        my_order_manager.placed_orders[:] = [my_order_manager.getOrder(
            order["id"]) for order in my_order_manager.placed_orders]

        print(my_order_manager.placed_orders)

        # Send a receipt.
        print("Fake receipt sent")

        response_message = "OK"
    else:
        response_message = "REQUEST FAILED"

    return response_message
