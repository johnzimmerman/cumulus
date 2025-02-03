<img src="cloud.png" alt="Cumbulus cloud" width="200"/>

# cumulus

A script to dollar-cost average cryptocurrency with the Coinbase Advanced Trade APIs

## Getting started

### Create an API key

You must have an (Advanced Trade) API key to get started with the Advanced Trade APIs. (You can no longer use Coinbase Pro keys.) See [Getting Started with Advanced Trade APIs](https://docs.cdp.coinbase.com/advanced-trade/docs/getting-started) for instructions.

Ensure you have the "Trade" permission checked.

![API permissions](trade_permission.png)

### Python, venv, and requirements.txt

1. Navigate to your project directory (e.g. `/home/<user>/cumulus`) and enter `python -m venv venv` This will create a virtual environment folder `venv`, which is ignored by `git`.

1. Activate the virtualenv with `source venv/bin/activate`

1. Install the dependencies within the virtualenv: `pip install -r requirements.txt`

### Edit the config file

1. Copy—don't just rename—the included example config file, `config.yml.example`, to `config.yml`. Your config file will be ignored by `git` and will remain on your system only.

1. Edit the config file. *Note: YAML is picky about spacing, so ensure your indentation stays consistent.*
    - Enter your API key and secret.
    - Enter the coins you want to buy and how much of each. You can add as many or as little as you like.

Cumulus is now installed, configured, and ready to run. Enter `./cumulus.py` or `python cumulus.py` to run it manually.

### Setup your cron

Next, set a cron job using `crontab -e` to run cumulus at your desired interval. Visit https://crontab.cronhub.io for a quick and simple editor that will help you build your cron expression.

#### Examples

1. `0 6 * * 5 /path/to/cumulus/venv/bin/python /path/to/cumulus/cumulus.py` - Runs 6:00 am server time every Fri

1. `* * * * * /path/to/cumulus/venv/bin/python /path/to/cumulus/cumulus.py` - Runs every min

### Profit!

## Helpful links

- [Introduction to Advanced Trade API](https://docs.cloud.coinbase.com/advanced-trade-api/docs/welcome)
- [Postman API Client](https://www.postman.com/product/api-client/) - Test API calls
