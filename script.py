from os import environ

import cbpro


# TODO: If the variables are in the ENV but empty, no warning is given
# https://www.twilio.com/blog/environment-variables-python
API_KEY = environ["CBPRO_KEY"]
API_SECRET = environ["CBPRO_SECRET"]
API_PASSPHRASE = environ["CBPRO_PASSPHRASE"]

if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE,
                                            api_url="https://api-public.sandbox.pro.coinbase.com")
    accounts = auth_client.get_accounts()
    print(accounts)
