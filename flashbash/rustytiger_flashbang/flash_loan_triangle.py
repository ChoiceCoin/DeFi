from algosdk import mnemonic
from algosdk.v2client import algod
from algofi_amm.v0.asset import Asset
from algofi_amm.v0.pool import Pool
from algofi_amm.v0.client import AlgofiAMMTestnetClient
from algofi_amm.v0.config import PoolType
from algofi_amm.utils import get_payment_txn, get_params, send_and_wait

myMnemonic = ""
sender = mnemonic.to_public_key(myMnemonic)
key =  mnemonic.to_private_key(myMnemonic)

algod_address = "http://127.0.0.1:4001"
algod_token = "a" * 64
algod_client = algod.AlgodClient(algod_token, algod_address)

amm_client = AlgofiAMMTestnetClient(user_address=sender, algod_client=algod_client)

ALGO_ID = 1
ALGO = Asset(amm_client, ALGO_ID)
USDC_ID = 51435943
USDC = Asset(amm_client, USDC_ID)
STBL_ID = 51437956
STBL = Asset(amm_client, STBL_ID)

# If not opt'd in, do so
for asset in [ALGO, USDC, STBL]:
    if not amm_client.is_opted_into_asset(asset):
        print(sender + " not opted into asset " + asset.name)
        params = get_params(amm_client.algod)
        txn = get_payment_txn(params, sender, sender, int(0), asset_id=asset.asset_id)
        send_and_wait(amm_client.algod, [txn.sign(key)])

# Triangle of pools
stbl_pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_30BP_FEE, STBL_ID, ALGO_ID)
pair_pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_30BP_FEE, STBL_ID, USDC_ID)
usdc_pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_30BP_FEE, USDC_ID, ALGO_ID)

# USDc pool has biggest algo reserve 
flash_loan_pool = usdc_pool

# Max loanable  amount
max_input_amount = flash_loan_pool.asset1_balance // 10 

def tryMakeProfit(pool1: Pool, pool2: Pool, pool3: Pool, input_amount: int):

    # Get pool prices
    quotes = []
    quotes.append(pool1.get_swap_exact_for_quote(ALGO_ID, input_amount))
    quotes.append(pool2.get_swap_exact_for_quote(pool1.asset2.asset_id, quotes[0].asset2_delta))
    if quotes[1].asset1_delta > 0:
        quotes.append(pool3.get_swap_exact_for_quote(pool3.asset2.asset_id, quotes[1].asset1_delta))
    else:
        quotes.append(pool3.get_swap_exact_for_quote(pool3.asset2.asset_id, quotes[1].asset2_delta))

    # Transaction fees for 3 swaps and a flash loan + flash loan pool fee
    swap_fees = 12000 + (input_amount // 1000) 
    
    # Make sure the profit outweighs the fees
    if (quotes[2].asset1_delta + quotes[0].asset1_delta) > swap_fees: 

        # Assemble transactions from quotes
        txnGroup = pool1.get_swap_exact_for_txns(sender, ALGO, -quotes[0].asset1_delta, quotes[0].asset2_delta)
        if quotes[1].asset1_delta > 0:
            txnGroup += pool2.get_swap_exact_for_txns(sender, pool1.asset2, -quotes[1].asset2_delta, quotes[1].asset1_delta)
        else:
            txnGroup += pool2.get_swap_exact_for_txns(sender, pool1.asset2, -quotes[1].asset1_delta, quotes[1].asset2_delta)
        txnGroup += pool3.get_swap_exact_for_txns(sender, pool3.asset2, -quotes[2].asset2_delta, input_amount + swap_fees)

        # Wrap in flash loan transactions
        flash_txns = flash_loan_pool.get_flash_loan_txns(sender, ALGO, input_amount + swap_fees, txnGroup)

        flash_txns.sign_with_private_key(sender, key)
       
        # Submit and hope no one beats you to it 
        try:
            flash_txns.submit(amm_client.algod, wait=True)
        except Exception as ex:
            # If transaction fails most likely price has moves since last block.
            print(f"Beaten to it {ex}")
    else:
        print("Not currently profitable")

# Try swapping the usdc and stbl pool and change the input value to get different opportunities 
tryMakeProfit(usdc_pool, pair_pool, stbl_pool, 20228200)
# Successful testnet group txn GmOCCn8RZ2gTihmWGZcmB6NQi6N//phZ86S65oPEQ3s=