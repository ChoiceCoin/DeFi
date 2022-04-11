from db.models import Trade

def get_trades(network: str, address: str):
    """Returns List of Trades To Be performed"""
    return Trade.objects(network=network, wallet_address=address, is_completed=False)




