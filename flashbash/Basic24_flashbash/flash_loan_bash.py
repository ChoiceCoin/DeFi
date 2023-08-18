
# 1. Import the necessary modules and Algofi Client for Mainnet
import os
from algosdk import mnemonic
from algofi_amm.v0.asset import Asset
from algofi_amm.v0.client import AlgofiAMMTestnetClient, AlgofiAMMMainnetClient
from algofi_amm.v0.config import PoolType, PoolStatus
from algofi_amm.utils import get_payment_txn, get_params, send_and_wait


sender = "WKS2Y7P7TFHKF6PEKWDFVWMHVBINSNTECH6HIP3YMW5KNQTB7T26DBDMWM"
key = mnemonic.to_private_key("stairs put example drop jealous spoil edge suggest hair choose depth festival salute crucial man expect slogan group title tiger goat fury basic absorb chapter")

IS_MAINNET = False
if IS_MAINNET:
    amm_client = AlgofiAMMMainnetClient(user_address=sender)
else:
    amm_client = AlgofiAMMTestnetClient(user_address=sender)

asset1_id = 1
asset2_id = 297995609


swap_input_asset = Asset(amm_client, asset1_id)
swap_asset_amount = 1000

flash_loan_asset = swap_input_asset
flash_loan_amount = 1000
min_amount_to_receive = 20

asset1 = Asset(amm_client, asset1_id)
asset2 = Asset(amm_client, asset2_id)

pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_25BP_FEE, asset1_id, asset2_id)
lp_asset_id = pool.lp_asset_id
lp_asset = Asset(amm_client, lp_asset_id)

if amm_client.get_user_balance(swap_input_asset) < swap_asset_amount:
    raise Exception(sender + " has insufficient amount of " + swap_input_asset.name + " to pool")
if pool.pool_status == PoolStatus.UNINITIALIZED:
    print("Pool has not been created + initialized")
else:
    swap_exact_for_txn = pool.get_swap_exact_for_txns(
        sender,
        swap_input_asset,
        swap_asset_amount,
        min_amount_to_receive=min_amount_to_receive,
    )
    
    flash_loan_txn = pool.get_flash_loan_txns(
        sender,
        swap_input_asset,
        flash_loan_amount,
        group_transaction=swap_exact_for_txn,
    )
    flash_loan_txn.sign_with_private_key(sender, key)
    flash_loan_txn.submit(amm_client.algod, wait=True)

print(f"Choice Flash Successful with\n{swap_input_asset}\n{min_amount_to_receive}")
