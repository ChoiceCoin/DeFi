from db.models import Trade, Asset

ass1 = Asset(name="Algo", asset_id="0", network="mainnet")
ass2 = Asset(name="Choice", asset_id="297995609", network="mainnet")

ass1.save()
ass2.save()

trade = Trade(
    wallet_address="Replace With Address",
    asset1=ass1,
    asset2=ass2,
    asset_in=ass2,
    asset_in_amount=10,
    slippage=0.5,
    min_sell_price=0.003,
    do_redeem=False,
    network="mainnet"
    )

trade.save()