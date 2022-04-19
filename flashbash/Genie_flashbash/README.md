# Choice Coin Flash loan Bash

### Exploiting an (ALGO/USDC) pool with a flash loan 


Made some changes to the tutorial code

Changed the pool variable to `pool = amm_client.get_pool(PoolType.CONSTANT_PRODUCT_30BP_FEE, asset1_id, asset2_id)`

`IS_MAINNET = False`

added `params=None` to swap_exact_for_txn and flash_loan_txn.

This is the link to the transaction on [Algoexplorer](https://testnet.algoexplorer.io/tx/FCUIMMVD3IKNYJ4FKNNRDFHUDIWUR4536MVG6C5P2AMIQLS2ACIA) 

You can look up the address used for this : S42RHBNDM2FJPW7NWBX6TQNBQJ7FE25QYO4ARUKPW2WQWTDJ42OPTY4BGA