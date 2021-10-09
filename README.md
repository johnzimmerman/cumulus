# cumulus

A script to dollar-cost average cryptocurrency on Coinbase Pro

## Code collaboration

- Download the [Live Share Extension Pack](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare-pack), a collection of extensions that enable real-time collaborative development with VS Live Share. From Microsoft.
- Follow the instructions under the Getting Started section of that page

## Getting started

1. Clone this repository.
1. Install the project dependencies.
    - Go to the directory where requirements.txt is located.
    - Activate your virtualenv.
    - Run: `pip install -r requirements_dev.txt` in your shell.
1. Create a Sandbox API key. Be sure to write down the passphrase and the secret because you won't be able to view them again.
1. Add the following environment variables to your machine using the information you wrote down above. The public key can be found on the web interface.
    - `CBPRO_PASSPHRASE=""`
    - `CBPRO_SECRET=""`
    - `CBPRO_KEY=""`
    - `CBPRO_API_URL=""` - **Only needs set in production.** The coinbase Pro API defaults to the production URL, but I think that's a bad idea so I set our script to use the sandbox URL by default.
1. Run: `./cumulus.py`. You should see a bunch of account info get printed to the screen if you set it up correctly.

## Sample order

The following payload will purchase $10 worth of BTC, $10 worth of ETH, and $5.00 worth of Polygon (MATIC)

```json
{
  "buy_orders": [
    {
      "product": "BTC-USD",
      "amount": 10.00
    },
    {
      "product": "ETH-USD",
      "amount": 10.00
    },
    {
      "product": "MATIC-USD",
      "amount": 5.00
    }
  ]
}
```

## Helpful links

- [coinbase Pro API documentation](https://docs.cloud.coinbase.com/exchange/docs) RECENTLY UPDATED
- Sandbox website: <https://public.sandbox.pro.coinbase.com>
- [coinbasepro-python library](https://github.com/danpaquin/coinbasepro-python)
- [Functions Framework for Python](https://github.com/GoogleCloudPlatform/functions-framework-python) - Test GCP functions locally
- [Postman API Client](https://www.postman.com/product/api-client/) - Test API calls

## Misc.

Deploy to production with the following:

`gcloud functions deploy cumulus-http-prod --entry-point cumulus_http --runtime python39 --trigger-http --env-vars-file .env.yaml  --service-account=cumulus-invoke@cumulus-317414.iam.gserviceaccount.com`
