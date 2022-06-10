from app.server.config.db import search_product_by_name
import json

async def search_product_by_keyword(keyword):
    """
    Search rating by keyword
    """
    products = await search_product_by_name(keyword)
    return products
    # return [ for product in products]


def search_product_by_url(url):
    """
    Search rating by url
    """
    pass


