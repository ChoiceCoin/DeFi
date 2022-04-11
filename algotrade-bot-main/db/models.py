import mongoengine
from mongoengine import fields
from mongoengine import connect


connect(db="tradebot", host="localhost", port=27017)


class Asset(mongoengine.Document):
    name = fields.StringField()
    asset_id = fields.StringField()
    network = fields.StringField()

class Trade(mongoengine.Document):
    wallet_address = fields.StringField()
    asset1 = fields.ReferenceField('Asset', reverse_delete_rule=2)
    asset2 = fields.ReferenceField('Asset', reverse_delete_rule=2)
    asset_in = fields.ReferenceField('Asset', reverse_delete_rule=2)
    asset_in_amt = fields.FloatField(min_value=0)
    slippage = fields.FloatField(min_value=0)
    min_sell_price = fields.FloatField(min_value=0)
    do_redeem = fields.BooleanField(default=True)
    is_completed = fields.BooleanField(default=False)
    do_reverse = fields.BooleanField(default=False)
    network = fields.StringField()
