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


if __name__ == "__main__":
    logging.info("Running cumulus.py")
    auth_client = cbpro.AuthenticatedClient(
        API_KEY, API_SECRET, API_PASSPHRASE,
        api_url=API_URL)
    accounts = auth_client.get_accounts()
    print(accounts)
