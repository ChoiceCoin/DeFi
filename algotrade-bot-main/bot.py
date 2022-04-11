from dataclasses import dataclass
import time
from tinyman.v1.client import TinymanTestnetClient, TinymanMainnetClient
from utils import get_trades
from colorama import Fore

@dataclass
class Account:
    """
    DataClass For Bot Account
    """
    address: str
    private_key: str

class Bot:

    def __init__(self, account: Account, network: str, interval: int):
        """
        Args:
            - account: Account object containing address and private_key
            - network: "testnet" or "mainnet".
            - trade: contains trade info
            - interval: sleeping interval for bot in milliseconds
        """
        self.account = account
        self.network = network
        self.interval = interval
        self.client = TinymanMainnetClient(user_address=account.address) if network == "mainnet" else TinymanTestnetClient(user_address=account.address)

    def run(self):
        print(Fore.GREEN, "Bot Is Running ...")
        if not self.client.is_opted_in():
            print(Fore.GREEN, "Optin In Progress ...")
            self._optin()
        while True:
            trades = get_trades(self.network, self.account.address)
            if not trades:
                print(Fore.RED, "No Trade To Execute")
                break
            for trade in trades:
                self._execute(trade)
            print(Fore.GREEN, f'Bot Sleeping For {self.interval} Seconds ...')
            time.sleep(self.interval)

    
    def _optin(self):
        """
        Opts In TinyMan App into Acount
        """
        transaction_group = self.client.prepare_app_optin_transactions()
        self._submit_txn(transaction_group)
        
    
    def _execute(self, trade):
        """
        Executes A Trade.
        Args:
            - trade: An Instance of Trade class in mongo db
        """
        t_asset1 = trade.asset1
        t_asset2 = trade.asset2
        t_asset_in = trade.asset_in
        asset1 = self.client.fetch_asset(int(t_asset1.asset_id))
        asset2 = self.client.fetch_asset(int(t_asset2.asset_id))
        pool = self.client.fetch_pool(asset1, asset2)
        if t_asset_in.asset_id != t_asset2.asset_id:
            quote = pool.fetch_fixed_input_swap_quote(
                    asset1(trade.asset_in_amt*10**asset1.decimals), float(trade.slippage))
        else:
            quote = pool.fetch_fixed_input_swap_quote(
                    asset2(trade.asset_in_amt*10**asset2.decimals), float(trade.slippage))
        amt_in = quote.amount_in_with_slippage
        amt_out = quote.amount_out_with_slippage
        amt_in = amt_in.amount/10**amt_in.asset.decimals
        amt_out = amt_out.amount/10**amt_out.asset.decimals
        price = amt_out/amt_in
        if price >= float(trade.min_sell_price):
            self._create_swap_txn(quote, pool)
            if trade.do_redeem:
                self._redeem(pool, t_asset_in, t_asset2, t_asset1)
            trade.is_completed = True
            trade.save()
        else:
            print(Fore.RED, f"Price Target Not Reached, Moving To The Next Trade...")
        

    
    def _create_swap_txn(self, quote, pool):
        transaction_group = pool.prepare_swap_transactions_from_quote(quote)
        self._submit_txn(transaction_group)
    
    def _redeem(self, pool, asset_in, asset2, asset1):
        excess = pool.fetch_excess_amounts()
        if asset_in.asset_id != asset2.asset_id:
            if asset2 in excess:
                self._submit_redeem(asset2, excess, pool)
                
        else:
            if asset1 in excess:
                self._submit_redeem(asset1, excess, pool)
    
    def _submit_redeem(self, asset, excess, pool):
        amount = excess[asset]
        transaction_group = pool.prepare_redeem_transactions(amount)
        self._submit_txn(transaction_group)
    
    def _submit_txn(self, txn):
        txn.sign_with_private_key(
            self.account.address, self.account.private_key)
        self.client.submit(txn, wait=True)
                
    
