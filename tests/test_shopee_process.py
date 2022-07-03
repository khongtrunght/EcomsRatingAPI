import pytest
import uplink

from server.crawler.Shopee import Shopee
from server.crawler.Ecom import EcomProcess
from server.crawler.Tiki import Tiki
from collections import defaultdict


@pytest.mark.asyncio
async def test_get_list_products():
    shop = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
    shop1 = Tiki(base_url='https://tiki.vn/api/v2/', client=uplink.AiohttpClient())
    shopee = EcomProcess(ecom=shop)
    query = defaultdict(keyword='áo', limit=10)
    products = await shopee.get_products_list(keyword='áo', limit=10)
    assert len(products) <= 10
    assert 'áo' in products[0].name.lower()


@pytest.mark.asyncio
async def test_get_ratings_for_product_part():
    shop = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
    shopee = EcomProcess(shop)
    product = {'itemid': '11148839378', 'name': 'áo', 'shopid': '105098362'}
    ratings = await shopee.get_ratings_for_product_part(product['itemid'], product['shopid'], offset=0, limit=50)
    assert len(ratings) <= 50


@pytest.mark.asyncio
async def test_get_ratings_for_product():
    shop = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
    shopee = EcomProcess(shop)
    product = {'itemid': '11148839378', 'name': 'áo', 'shopid': '105098362'}
    ratings = await shopee.get_ratings_for_product(product['itemid'], product['shopid'])
    assert len(ratings) <= 300
