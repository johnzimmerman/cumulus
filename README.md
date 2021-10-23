# cumulus

A script to dollar-cost average cryptocurrency on Coinbase Pro

## Getting started

### Git & GitHub

1. Check that you have `git` installed by running `git` in the terminal. If it's installed, move on to the next step. If your system returns `git: command not found,` install `git` with `sudo apt-get install git`

1. Next, generate an SSH key by typing `ssh-keygen -t ed25519` You can choose whether or not to use a passphrase. This key will be used to pull the code from GitHub to your server.

1. Send me your **public key**

1. Once I've added your public key to the list of deploy keys, go to the directory where where you want cumulus installed and run, `git clone git@github.com:johnzimmerman/cumulus.git` This will download the source code to your computer.

### Python and virtualenv

1. Check that you have `virtualenv` installed by running `virtualenv` in the terminal. If it's installed, move on to the next step. Otherwise, install it by running, `apt-get install python3-virtualenv`

1. Navigate to your project directory (e.g. `/home/<user>/cumulus`) and enter `virtualenv venv` This will create a virtual environment folder `venv`, which is ignored by `git`.

1. Activate the virtualenv with `source venv/bin/activate`

1. Install the dependencies within the virtualenv: `pip install -r requirements.txt`

### Edit the config file

1. Copy—don't just rename—the included example config file, `config.yml.example`, to `config.yml` by typing `cp config.yml.example config.yml` in your terminal. Your config file will be ignored by `git` and will remain on your system only.

1. Edit the config file. *Note: YAML is picky about spacing, so ensure your indentation stays consistent.*
    - Enter your API key, secret, and passphrase for each Coinbase Pro environment (sandbox and production).
    - Enter the coins you want to buy and how much of each. You can add as many or as little as you like.

Cumulus is now installed, configured, and ready to run. Enter `./cumulus.py` to test it. By default, cumulus runs in the sandbox environment. If you want to run it in production (with real money), enter `./cumulus.py --production`

### Setup your cron

Next, set a cron job using `crontab -e` to run cumulus at your desired interval. Visit https://crontab.cronhub.io for a quick and simple editor that will help you build your cron expression.

#### Examples

1. **Production:** `0 6 * * 5 /path/to/cumulus/venv/bin/python /path/to/cumulus/cumulus.py --production` - Runs 6:00 am server time every Fri

1. **Sandbox:** `* * * * * /path/to/cumulus/venv/bin/python /path/to/cumulus/cumulus.py` - Run every min

### Profit!

### Updating cumulus

To be filled out when I actually update it.

1. Create a Sandbox API key. Be sure to write down the passphrase and the secret because you won't be able to view them again.

1. Run: `./cumulus.py`. You should see a bunch of account info get printed to the screen if you set it up correctly.

## Helpful links

- [coinbase Pro API documentation](https://docs.cloud.coinbase.com/exchange/docs) RECENTLY UPDATED
- Sandbox website: <https://public.sandbox.pro.coinbase.com>
- [coinbasepro-python library](https://github.com/danpaquin/coinbasepro-python)
- [Postman API Client](https://www.postman.com/product/api-client/) - Test API calls

## Code collaboration

- Download the [Live Share Extension Pack](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare-pack), a collection of extensions that enable real-time collaborative development with VS Live Share. From Microsoft.
- Follow the instructions under the Getting Started section of that page
