import asyncio
import pprint

import motor.motor_asyncio
# from products.product import *
from typing import List, Dict
import datetime
from server.schemas.rating import Product

# import nest_asyncio

# nest_asyncio.apply()
# client = None

conn_str = "mongodb+srv://chau25102001:chau25102001@cluster0.pxxj2.mongodb.net/?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS = 5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client.test


async def insert_one_product(product):
    # product = locals()
    # product.date = datetime.datetime.now()
    source = product.source
    item_id = product.item_id
    shop_id = product.shop_id
    in_DB = await check_in_DB(item_id, shop_id, source)
    if not in_DB:
        await db.products.insert_one(document=product.dict())
        return True
    else:
        return False


async def insert_many_products(products: List[Product]):
    success_count = 0
    for p in products:
        kq = await insert_one_product(p)
        success_count += 1 if kq else 0

    return dict(success_count=success_count, total_count=len(products))

    # return "Alo"


async def check_in_DB(item_id: str = None, shop_id: str = None, source: str = None) -> bool:
    # assert source in ['tiki', 'lazada', 'shoppee'], "Only support either tiki, lazada, or shoppee"
    assert item_id is not None and source is not None, "At least one of item_id or source must be not None"

    async def fetch_products():
        prods = await db.products.find_one({"source": {"$regex": source},
                                            "item_id": {"$regex": item_id},
                                            "shop_id": {"$regex": shop_id}})
        return prods

    prods = await fetch_products()
    if prods is not None:
        return True
    else:
        return False


async def search_product_by_name(name: str, limit: int = 5):
    assert name is not None and len(name) != 0, "Name cannot be None or empty"
    result = []

    async def fetch_products():
        prods = db.products.find({"name": {"$regex": name, "$options": 'i'}}, {'reviews': {"$slice": 5}})
        for doc in await prods.to_list(length = limit):
            result.append(doc)
        await db.products.update_many({"name": {"$regex": name, "$options": 'i'}}, {
            "$inc": {"query_times": 1}
        })

    # loop = client.get_io_loop()
    await fetch_products()
    return result


async def search_products_by_ids(item_id: str, shop_id: str, source: str, length: int = 5):
    result = []

    async def fetch_products():
        prods = db.products.find({"source": {"$regex": source, "$options": 'i'},
                                  "item_id": {"$regex": item_id},
                                  "shop_id": {"$regex": shop_id}}, {'reviews': {"$slice": 5}})
        for doc in await prods.to_list(length = length):
            result.append(doc)
        await db.products.update_many({"source": {"$regex": source, "$options": 'i'},
                                       "item_id": {"$regex": item_id},
                                       "shop_id": {"$regex": shop_id}}, {
                                          "$inc": {"query_times": 1}
                                      })

    await fetch_products()
    return result


async def delete_products_by_ids(item_id: str, shop_id: str, source: str):
    async def delete_products():
        n = await db.products.count_documents({})
        await db.products.delete_many({"source": {"$regex": source, "$options": 'i'},
                                       "item_id": {"$regex": item_id},
                                       "shop_id": {"$regex": shop_id}})
        return (
            f"Number of products before deletion: {n}\nNumber of products after deletion: {await db.products.count_documents({})}")

    # loop = client.get_io_loop()
    # loop.run_until_complete(delete_products())
    await delete_products()


async def summary_products():
    result = []

    async def fetch_all():
        prods = db.products.aggregate([
            # {"$unwind": "$reviews"},
            {"$unset": ["_id"]},
            {"$project": {
                "name": "$name",
                "item_id": "$item_id",
                "shop_id": "$shop_id",
                "source": "$source",
                "avg_rating": {"$avg": "$reviews.rating"},
                # "avg_rating": "$avg_rating",
                "query_times": "$query_times"
            }},

        ])
        for p in await prods.to_list(length = None):
            result.append(p)
        return result

    # loop = client.get_io_loop()
    # loop.run_until_complete(fetch_all())
    await fetch_all()
    return result


async def close_db():
    client.close()

# pprint.pprint(search_product_by_name('chuột'))
