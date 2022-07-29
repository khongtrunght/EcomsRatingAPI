from server.config.db import insert_many_products, insert_one_product
from server.crawler.Shopee import Shopee
from server.crawler.Ecom import Ecom
from server.crawler.Tiki import Tiki
from server.config.db import delete_products_by_ids, summary_products
from server.schemas.rating import Product, ShopeeItem
import numpy as np

ecom = Ecom()

async def crawl_by_keyword(keyword: str, limit: int):
    # shopee = Shopee('https://shopee.vn')
    # tiki = Tiki('https://tiki.vn/')
    # r1 = shopee.find_reviews_by_keyword(keyword)
    # insert_many_products(r1)
    # r2 = tiki.find_reviews_by_keyword(keyword)
    # insert_many_products(r2)

    r1 = await ecom.search_product_by_keyword(keyword=keyword, limit=limit)
    rsp_products = [
        Product(
            item_id=product.itemid,
            shop_id=product.shopid,
            name=product.name,
            source='shopee' if isinstance(product, ShopeeItem) else 'tiki',
            reviews=product.ratings,
            avg_rating = np.average([r.rating for r in product.ratings])
        )
        for product in r1
    ]

    return await insert_many_products(rsp_products)




async def crawl_by_url(url: str):
    r1 = await ecom.search_product_by_url(url)
    rsp_product = Product(
        item_id=r1.itemid,
        shop_id=r1.shopid,
        name=r1.name,
        source='shopee' if isinstance(r1, ShopeeItem) else 'tiki',
        reviews=r1.ratings,
        avg_rating = np.average([r.rating for r in r1.ratings])
    )
    return await insert_one_product(rsp_product)


async def crawl_by(data: str, by: str, limit: int):
    if by == 'keyword':
        rsp = await crawl_by_keyword(data, limit)
        return {
            'status': 'success',
            'num_product_success': rsp['success_count'],
            'duplicate_db': rsp['total_count'] - rsp['success_count'],
        }
    elif by == 'url':
        rsp = await crawl_by_url(data)
        return {
            'status': 'success',
            'num_product_success': 1 if rsp else 0,
            'duplicate_db': 0 if rsp else 1,
        }



async def delete_products(item_id: str, shop_id: str, source: str, by = "id"):
    assert by == "id", "Only support delete by id"
    if by == 'id':
        return await delete_products_by_ids(item_id, shop_id, source)
    else:
        return "Nothing happen!!!"


async def summary_all_products():
    return await summary_products()
