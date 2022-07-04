import pytest
import uplink

from server.crawler.Shopee import Shopee
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


@pytest.mark.asyncio
async def test_search_product_by_keyword():
	shopee = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
	products = await shopee.search_product_by_keyword(**dict(keyword='áo', limit=10))
	# products = await products.json()
	LOGGER.info(f"Shopee Products: {products}")


@pytest.mark.asyncio
async def test_get_ratings_for_product():
	shopee = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
	rqt = shopee.get_convert_ratings(itemid=10737792056, shopid=276087485, offset=0, limit=5)
	ratings = await shopee.get_rating_list(**rqt)
	print(ratings)


@pytest.mark.asyncio
async def test_get_product_by_url():
	url =  "https://shopee.vn/%C3%81o-Thun-Nam-N%E1%BB%AF-Tay-L%E1%BB%A1-1998-Form-R%E1%BB%99ng-Unisex-Ulzzang-i.276087485.10737792056?sp_atk=0a2e1bc5-d9a6-46cc-a63e-2445f72dbbe5&xptdk=0a2e1bc5-d9a6-46cc-a63e-2445f72dbbe5"
	shopee = Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
	product = await shopee.get_product_by_url(url)
	assert len(product.ratings) > 0
	LOGGER.info(f"Shopee Product: {product}")
