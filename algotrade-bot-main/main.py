import os
from bot import Bot, Account
from algosdk import mnemonic
from dotenv import load_dotenv
load_dotenv()

address = os.getenv("ADDRESS")
key = mnemonic.to_private_key(os.getenv("KEY"))

account = Account(address, key)
bot = Bot(account, "mainnet", 5) #Run Bot On TestNet With 5 seconds interval
bot.run()
