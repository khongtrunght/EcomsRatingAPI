from server.config.db import insert_many_products
from server.crawler.Shopee import Shopee, Ecom
from server.crawler.Tiki import Tiki
from server.config.db import delete_products_by_ids, summary_products
from server.schemas.rating import Product, ShopeeItem


async def crawl_by_keyword(keyword: str):
    # shopee = Shopee('https://shopee.vn')
    # tiki = Tiki('https://tiki.vn/')
    # r1 = shopee.find_reviews_by_keyword(keyword)
    # insert_many_products(r1)
    # r2 = tiki.find_reviews_by_keyword(keyword)
    # insert_many_products(r2)
    ecom = Ecom()
    r1 = await ecom.search_product_by_keyword(keyword=keyword, limit=2)
    rsp_products = [
        Product(
            item_id=product.itemid,
            shop_id=product.shopid,
            name=product.name,
            source='shopee' if isinstance(product, ShopeeItem) else 'tiki',
            reviews=product.ratings,
        )
        for product in r1
    ]

    await insert_many_products(rsp_products)




def crawl_by_url(url: str):
    if 'shopee' in url:
        shopee = Shopee('https://shopee.vn')
        results = shopee.find_reviews_by_url(url)
        print(results)
        # for res in results:
        insert_many_products(results)
    elif 'tiki' in url:
        tiki = Tiki('https://tiki.vn/')
        results = tiki.find_reviews_by_url(url)
        print(results)
        insert_many_products(results)
    else:
        print("Nothing happen!!!")


async def crawl_by(data: str, by: str):
    if by == 'keyword':
        return await crawl_by_keyword(data)
    elif by == 'url':
        return crawl_by_url(data)



async def delete_products(item_id: str, shop_id: str, source: str, by = "id"):
    assert by == "id", "Only support delete by id"
    if by == 'id':
        return await delete_products_by_ids(item_id, shop_id, source)
    else:
        return "Nothing happen!!!"


async def summary_all_products():
    return await summary_products()
