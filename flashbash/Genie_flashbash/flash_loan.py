import os
from dotenv import dotenv_values
from algosdk import mnemonic
from algofi_amm.v0.asset import Asset
from algofi_amm.v0.client import AlgofiAMMTestnetClient, AlgofiAMMMainnetClient
from algofi_amm.v0.config import PoolType, PoolStatus
from algofi_amm.utils import get_payment_txn, get_params, send_and_wait


my_path = os.path.abspath(os.path.dirname(__file__))
ENV_PATH = os.path.join(my_path, ".env")
user = dotenv_values(ENV_PATH)
sender = mnemonic.to_public_key(user['mnemonic'])
key =  mnemonic.to_private_key(user['mnemonic'])



IS_MAINNET = False
if IS_MAINNET:
    amm_client = AlgofiAMMMainnetClient(user_address=sender)
else:
    amm_client = AlgofiAMMTestnetClient(user_address=sender)

# SET POOL ASSETS + AMOUNTS
asset1_id = 1
asset2_id = 10458941
swap_input_asset = Asset(amm_client, asset1_id)
swap_asset_amount = 100
flash_loan_asset = swap_input_asset
flash_loan_amount = 100
min_amount_to_receive=2
asset1 = Asset(amm_client, asset1_id)
asset2 = Asset(amm_client, asset2_id)
pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_30BP_FEE, asset1_id, asset2_id)
lp_asset_id = pool.lp_asset_id
lp_asset = Asset(amm_client, lp_asset_id)

# make sure user is opted in and has balance
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
    raise Exception(sender + " has insufficient amount of " + swap_input_asset.name + " to pool")

if pool.pool_status == PoolStatus.UNINITIALIZED:
    print("Pool has not been created + initialized")
else:
    swap_exact_for_txn = pool.get_swap_exact_for_txns(sender, swap_input_asset, swap_asset_amount, min_amount_to_receive=min_amount_to_receive,  params=None)
    flash_loan_txn = pool.get_flash_loan_txns(sender, swap_input_asset, flash_loan_amount, group_transaction=swap_exact_for_txn,  params=None)
    
    print(sender, swap_input_asset, min_amount_to_receive)

    flash_loan_txn.sign_with_private_key(sender, key)
    flash_loan_txn.submit(amm_client.algod, wait=True)

