import os
from dotenv import load_dotenv

from algosdk import mnemonic, error
from algofi_amm.v0.asset import Asset
from algofi_amm.utils import get_params, get_payment_txn, send_and_wait
from algofi_amm.v0.client import AlgofiAMMTestnetClient, AlgofiAMMMainnetClient
from algofi_amm.v0.config import PoolType, PoolStatus

load_dotenv()


IS_MAINNET = True


class FlaskLoan(object):
    def __init__(self, mnemonic_data: str):
        try:
            self.mnemonic_data = mnemonic_data  ## MNEMONIC DATA
            ## PUBLIC WALLET ADDRESS
            self.myAddress = mnemonic.to_public_key(mnemonic_data)
            ## PRIVATE KEY
            self.private_key = mnemonic.to_private_key(self.mnemonic_data)

            ## ALGOD CLIENT
            if not IS_MAINNET:
                self.amm_client = AlgofiAMMTestnetClient(user_address=self.myAddress)
            else:
                self.amm_client = AlgofiAMMMainnetClient(user_address=self.myAddress)

            ## ASSET IDS
            self.asset_id = 1  # Asset AlGO
            self.asset2_id = 297995609  ## ASSET CHOICE
            # self.asset2_id = 10458941 ## TESTNET USDC ASSET

            # ASSETS
            self.input_asset = Asset(self.amm_client, self.asset_id)
            self.output_asset = Asset(self.amm_client, self.asset2_id)
            self.swap_amount = 2  # 2 Algo

            # FLASH ASSET AND AMOUNT
            self.flash_asset = self.input_asset
            self.flash_amount = 2  # 2 Choice

            # Converts amount to valid
            if IS_MAINNET:
                self.swap_newamount = self.swap_amount * 1000000
                self.flash_newamount = self.flash_amount * 1000000
            else:
                self.swap_newamount = self.swap_amount * 100000
                self.flash_newamount = self.flash_amount * 100000

            # OTHERS
            self.min_amount_to_receive = 5
            self.pool = None
            self.asset_balance = 0
            self.asset2_balance = 0
        except Exception as e:
            print(f"An error occured: {str(e)}")
            exit(1)

    ## GET USER INPUT IF NOT ASSET IN ACCOUNT
    def get_input(self, data: str):
        user_input = input(data)
        return user_input.lower()

    def create_pool(self):
        print("Creating poool...")
        if IS_MAINNET:
            self.pool = self.amm_client.get_pool(
                PoolType.CONSTANT_PRODUCT_75BP_FEE, self.asset_id, self.asset2_id
            )
        else:
            self.pool = self.amm_client.get_pool(
                PoolType.CONSTANT_PRODUCT_30BP_FEE, self.asset_id, self.asset2_id
            )
        print("Created pool successfully")

    def check_if_opted_into_asset(self, asset_id, asset):
        try:
            print(f"Checking if user is opted into asset: {asset.name}")
            if not self.amm_client.is_opted_into_asset(asset):
                print("User not opted into asset")
                if self.get_input(
                    f"Do you want to opt into asset: {asset.name}:{asset_id} [y/n]: "
                ).startswith("y"):
                    params = get_params(self.amm_client.algod)
                    txn = get_payment_txn(
                        params,
                        self.myAddress,
                        self.myAddress,
                        int(0),
                        asset_id=asset_id,
                    )
                    print("Creating asset transaction....")
                    txn = send_and_wait(
                        self.amm_client.algod, [txn.sign(self.private_key)]
                    )
                else:
                    print("Exiting program...")
                    exit(0)
            else:
                print("User is opted into asset")
        except error.IndexerHTTPError as e:
            print(f"An error occured: {str(e)}")
            exit(1)

    def loan(self):
        if IS_MAINNET:
            print(
                f"Swapping {self.swap_amount} {self.input_asset.name} to {self.output_asset.name}"
            )
        else:
            print(
                f"Swapping {self.swap_amount / 10} {self.input_asset.name} to {self.output_asset.name}"
            )
        if self.pool.pool_status == PoolStatus.UNINITIALIZED:
            print("Pool has not been Initialized \nExiting....")
            exit(1)
        if self.asset_balance < self.swap_amount:
            print(
                f"You have insufficient fund to swap your {self.input_asset.name} to {self.output_asset.name} \nExiting..."
            )
            exit(1)
        swap_txn = self.pool.get_swap_exact_for_txns(
            self.myAddress,
            self.input_asset,
            self.swap_newamount,
            min_amount_to_receive=2,
        )
        flash_loan_txn = self.pool.get_flash_loan_txns(
            self.myAddress,
            self.input_asset,
            self.flash_newamount,
            group_transaction=swap_txn,
        )
        print("Signing flash")
        flash_loan_txn.sign_with_private_key(self.myAddress, self.private_key)
        print("Signed! Waiting for confirmation")
        txn = flash_loan_txn.submit(self.amm_client.algod, wait=True)
        return txn

    def get_balance(self):
        print("Querying balance on assets")
        self.asset_balance = self.amm_client.get_user_balance(self.input_asset)
        self.asset2_balance = self.amm_client.get_user_balance(self.output_asset)
        print("#######################################################")
        print(
            f"You have a balance of {self.asset_balance} on asset: {self.input_asset.name}"
        )
        print(
            f"You have a balance of {self.asset2_balance} on asset: {self.output_asset.name}"
        )
        print("#######################################################")

    def run(self):
        print(f"Got your address as: {self.myAddress}")
        self.check_if_opted_into_asset(self.asset_id, self.input_asset)
        self.check_if_opted_into_asset(self.asset2_id, self.output_asset)
        self.get_balance()
        self.create_pool()
        txn = self.loan()
        print(self.input_asset, self.min_amount_to_receive)
        print("Flash loan completed successfully")
        print("\n\n")
        if IS_MAINNET:
            print(f"Check transaction at https://algoexplorer.io/tx/{txn['txid']}")
        else:
            print(
                f"Check transaction at https://testnet.algoexplorer.io/tx/{txn['txid']}"
            )


def main():
    print("Running...")
    flask_loan = FlaskLoan(os.getenv("mnemonic"))
    flask_loan.run()


if __name__ == "__main__":
    main()
