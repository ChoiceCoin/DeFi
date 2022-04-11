
# Algorand Trading Bot

This is A Trading Bot That Allows swapping an asset to another at a set price. It stores list of trades in a mongo db.

At the moment this bot integrates with the following DEXs:

- [Tinyman](https://tinyman.org/)

## Development Status

This bot is currently under active early development and has not yet been audited. It should therefore not be considered stable.

## Development Setup

This repo requires Python 3.7 or higher. We recommend you use a Python virtual environment to install the required dependencies.

Set up venv (one time):

- `python3 -m venv venv`

Active venv:

- `. venv/bin/activate` (if your shell is bash/zsh)
- `. venv/bin/activate.fish` (if your shell is fish)

Install dependencies:

- `pip install -r requirements.txt`

The `tinyman-py-sdk` package is also needed but it is not yet released on PYPI. It can be installed directly from the tinyman-py-sdk repository with pip:

`pip install git+https://github.com/tinymanorg/tinyman-py-sdk.git`

Mongo DB has to be installed on your system, this stores the trades and assets. click here https://www.mongodb.com/try/download/community To install Mongo DB for Your OS.

## Off-chain DB

This bot is implemented to make use of an off-chain MongoDB database that currently contains two tables:

- The `assets` table holds token identification details of the Algorand native token and Algorand Standard Assets (ASAs) that can be traded with the bot.
- The `trades` table is where the bot looks for trade requests you want performed on behalf of your Algorand wallet.

Schema definitions for these tables can be found in the file [db/models.py](./db/models.py).

To Create An Asset and Trade, Visit the [populate.py](./populate.py) File For Code Samples.

## Model Schema Definition

```
class Asset:
    name: "name of the asset"
    asset_id: "asa id e.g(0) for Algorand"
    network: "mainnet" or "testnet"

class Trade:
    wallet_address: "Algorand Wallet Address of The Trade Executor"
    asset1: Asset object (e.g Asset(name="Algorand"))
    asset2: Asset objects
    asset_in: Asset To swap
    asset_in_amt: Amount of Asset In To Swap
    slippage: TinyMan Slippage
    min_sell_price: Minimum Price to sell Asset for e.g (Sell choice for Algo for at least 0.003 Algo Per choice)
    do_redeem: Boolean for redeeming excess assets
    network: "mainnet" or "testnet"
```

## Environment Variables

There are environment variables that need to be properly configured for the bot to work. Create a file named `.env` in the ptoject root folder and copy the contents of `.env.example` to it, then set the variables in **.env** to appropriate values.

## Launching the bot (to run every X seconds)

To Run the bot, edit the `Bot` object in the [main.py](./main.py) file and run `python main.py`.

### Sample Code To Run Bot
```
import os
from bot import Bot, Account
from algosdk import mnemonic
from dotenv import load_dotenv
load_dotenv()

address = os.getenv("ADDRESS") #Address In ENV File
key = mnemonic.to_private_key(os.getenv("KEY")) #Mnemonic In ENV File

account = Account(address, key)
bot = Bot(account, "mainnet", 5) #Run Bot On MainNet With 5 seconds interval
bot.run()
```

