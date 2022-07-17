from server.config.db import search_product_by_name, search_products_by_ids
import re
import urllib

async def search_product_by_keyword(keyword, limit):
    """
    Search rating by keyword
    """
    products = await search_product_by_name(keyword, limit)
    return products
    # return [ for product in products]


async def search_product_by_url(url):
    """
    Search rating by url
    """
    r = None
    url = urllib.parse.unquote(url)
    source = ""
    shop_id = ""
    item_id = ""
    if 'shopee' in url:
        r = re.search(r"i\.(\d+)\.(\d+)", url)
        source = 'shopee'
        shop_id, item_id = r[1], r[2]
    elif 'tiki' in url:
        r = re.search(r"p(\d+).", url)
        source = 'tiki'
        item_id = r[0][1:-1]

    products = await search_products_by_ids(item_id, shop_id, source)
    return products
