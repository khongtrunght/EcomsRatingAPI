from app.server.config.db import search_product_by_name
import json

def search_product_by_keyword(keyword):
    """
    Search rating by keyword
    """
    products = search_product_by_name(keyword)
    return [json.loads(product.to_json()) for product in products]


def search_product_by_url(url):
    """
    Search rating by url
    """
    pass


