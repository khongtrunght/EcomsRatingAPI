import pytest
import uplink

from server.crawler.Shopee import Shopee


@pytest.mark.asyncio
async def test_search_product_by_keyword():
    shopee = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
    products = await shopee.search_product_by_keyword(**dict(keyword='áo', limit=10))
    # products = await products.json()
    print(products)

@pytest.mark.asyncio
async def test_get_ratings_for_product():
    shopee = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
    ratings = await shopee.get_rating_list(**dict(product_id='135507987', seller_id='191464'))
    print(ratings)


