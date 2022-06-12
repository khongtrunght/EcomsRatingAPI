import pytest
import uplink

from server.crawler.Shopee import Tiki


@pytest.mark.asyncio
async def test_search_product_by_keyword():
    tiki = Tiki(base_url='https://tiki.vn/api/v2/', client=uplink.AiohttpClient())
    products = await tiki.search_product_by_keyword(**dict(q='áo', limit=10))
    print(products)

@pytest.mark.asyncio
async def test_get_ratings_for_product():
    tiki = Tiki(base_url='https://tiki.vn/api/v2/', client=uplink.AiohttpClient())
    ratings = await tiki.get_rating_list(**dict(product_id='135507987', seller_id='191464'))
    print(ratings)



