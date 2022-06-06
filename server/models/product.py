import datetime

import mongoengine
from .reviews import Review


class Product(mongoengine.Document):
    name = mongoengine.StringField(required=True)  # product name
    item_id = mongoengine.StringField(default=None)
    shop_id = mongoengine.StringField(default=None)
    source = mongoengine.StringField(default=None)  # source website of the products, either Shoppee, Lazada, or Tiki
    date = mongoengine.DateTimeField(default=datetime.datetime.now)  # when is product added into database
    query_times = mongoengine.IntField(default=0)  # how many times products are queried
    reviews = mongoengine.EmbeddedDocumentListField(Review)
    available = mongoengine.BooleanField(default=True)  # Are we selling this product
    meta = {
        'db_alias': 'SE_DB',
        'collection': 'products'
    }
