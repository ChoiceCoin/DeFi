#Type python flash_loan.py in a directory with all the runsteps to run this file
#Be sure to enter your mnemonic and address as required.

#Overview
#This tutorial is a guide to using Algofi to obtain Flash Loan. 
#The flash_loan is meant to allow individuals in the Algorand Ecosystem to obtain any asset through flash loan directly through their terminal.

# Requirements
##################################
# All requirements for this Tutorial can be found in the [requirements.txt](https://github.com/ChoiceCoin/Flash_loan/blob/main/requirements.txt) file on the Choice Coin GitHub. 

# To install the requirements run: 

# pip install requirements.txt


# Steps 
##################################

# 1. Import the necessary modules and Algofi Client for Mainnet
import os
from dotenv import dotenv_values
from algosdk import mnemonic
from algofi_amm.v0.asset import Asset
from algofi_amm.v0.client import AlgofiAMMTestnetClient, AlgofiAMMMainnetClient
from algofi_amm.v0.config import PoolType, PoolStatus
from algofi_amm.utils import get_payment_txn, get_params, send_and_wait

# 2. Copy your address and mnemonic here, which can be found in your Algorand Wallet or
#   import 25 char mnemonic from .env file
#   Fund the account for mnemonic with ALGO +  ASAs

user = dotenv_values(".env")
sender = mnemonic.to_public_key(user["mnemonic"])
key = mnemonic.to_private_key(user["mnemonic"])

# 3.  Setup Algofi AMM Clients to Mainnet or Testnet

IS_MAINNET = True
if IS_MAINNET:
    amm_client = AlgofiAMMMainnetClient(user_address=sender)
else:
    amm_client = AlgofiAMMTestnetClient(user_address=sender)

# 4. SET POOL ASSETS + AMOUNTS
#  Default Algo is set to 1, You can change to any ASSET PAIRS pools you want to take the flashloan from.

asset1_id = 1
asset2_id = 297995609

# 5. Swap Input Asset

swap_input_asset = Asset(amm_client, asset1_id)
swap_asset_amount = 100

# 6. Flash Loan Asset

flash_loan_asset = swap_input_asset
flash_loan_amount = 100     # Amount to be borrowed on Flash loan

min_amount_to_receive = 2  # Txn fee

# 7. Gets Asset-Pair details
asset1 = Asset(amm_client, asset1_id)
asset2 = Asset(amm_client, asset2_id)

# 8. Gets the pool in terms of the assets with given asset_ids
#  You can borrow up to 10% of asset in a pool
pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_25BP_FEE, asset1_id, asset2_id)

lp_asset_id = pool.lp_asset_id
lp_asset = Asset(amm_client, lp_asset_id)

# 9. make sure user is opted in and has balance
if not amm_client.is_opted_into_asset(asset1):
    print(sender + " not opted into asset " + asset1.name)
    params = get_params(amm_client.algod)
    txn = get_payment_txn(params, sender, sender, int(0), asset_id=asset1.asset_id)
    send_and_wait(amm_client.algod, [txn.sign(key)])

if not amm_client.is_opted_into_asset(asset2):
    print(sender + " not opted into asset " + asset2.name)
    params = get_params(amm_client.algod)
    txn = get_payment_txn(params, sender, sender, int(0), asset_id=asset2.asset_id)
    send_and_wait(amm_client.algod, [txn.sign(key)])


if amm_client.get_user_balance(swap_input_asset) < swap_asset_amount:
    raise Exception(
        sender + " has insufficient amount of " + swap_input_asset.name + " to pool"
    )

if pool.pool_status == PoolStatus.UNINITIALIZED:
    print("Pool has not been created + initialized")
    
else:
    swap_exact_for_txn = pool.get_swap_exact_for_txns(
        sender,
        swap_input_asset,
        swap_asset_amount,
        min_amount_to_receive=min_amount_to_receive,
    )

    # Algofi Flash loan Transaction
    flash_loan_txn = pool.get_flash_loan_txns(
        sender,
        swap_input_asset,
        flash_loan_amount,
        group_transaction=swap_exact_for_txn,
    )
    flash_loan_txn.sign_with_private_key(sender, key)
    flash_loan_txn.submit(amm_client.algod, wait=True)
