import asyncio
import pprint

import motor.motor_asyncio
# from products.product import *
from typing import List, Dict
import datetime

client = None

conn_str = "mongodb+srv://chau25102001:chau25102001@cluster0.pxxj2.mongodb.net/?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS = 5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client.test


# print(r)


def insert_one_product(product):
    # product = locals()
    product['date'] = datetime.datetime.now()

    async def do_insert():
        result = await db.products.insert_one(document = product)
        print('result %s' % repr(result.inserted_id))

    loop = client.get_io_loop()
    loop.run_until_complete(do_insert())


def insert_many_products(products: List[Dict]):
    for p in products:
        name = p['name']
        source = p['source']
        item_id = p['item_id']
        shop_id = p['shop_id']
        reviews = p['reviews']

        in_DB = check_in_DB(item_id, shop_id, source)
        if not in_DB:
            insert_one_product(p)
        else:
            continue


def check_in_DB(item_id: str = None, shop_id: str = None, source: str = None) -> bool:
    # assert source in ['tiki', 'lazada', 'shoppee'], "Only support either tiki, lazada, or shoppee"
    assert item_id is not None and source is not None, "At least one of item_id or source must be not None"

    async def fetch_products():
        prods = await db.products.find_one({"source": {"$regex": source},
                                            "item_id": {"$regex": item_id},
                                            "shop_id": {"$regex": shop_id}})
        return prods

    loop = client.get_io_loop()
    prods = loop.run_until_complete(fetch_products())
    if prods is not None:
        return True
    else:
        return False


async def search_product_by_name(name: str):
    assert name is not None and len(name) != 0, "Name cannot be None or empty"
    result = []

    async def fetch_products():
        prods = db.products.find({"name": {"$regex": name, "$options": 'i'}}, {'reviews': {"$slice": 5}})
        for doc in await prods.to_list(length = 100):
            result.append(doc)

    # loop = client.get_io_loop()
    await fetch_products()
    return result


def search_products_by_ids(item_id: str, shop_id: str, source: str):
    result = []

    async def fetch_products():
        prods = db.products.find({"source": {"$regex": source, "$options": 'i'},
                                  "item_id": {"$regex": item_id},
                                  "shop_id": {"$regex": shop_id}}, {'reviews': {"$slice": 5}})
        for doc in await prods.to_list(length = 100):
            result.append(doc)

    loop = client.get_io_loop()
    loop.run_until_complete(fetch_products())
    return result


prods = search_product_by_name("Chuột Không Dây Logitech M221 - Hàng Chính Hãng")
print(prods)
