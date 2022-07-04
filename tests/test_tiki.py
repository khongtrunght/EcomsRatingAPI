import pytest
import uplink
import logging
from server.crawler.Tiki import Tiki

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


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


@pytest.mark.asyncio
async def test_get_product_by_url():
	url = "https://tiki.vn/apple-iphone-13-pro-hang-chinh-hang-p184058811.html?i=40395&itm_campaign=tiki-reco_UNK_DT_UNK_UNK_infinite-scroll_infinite-scroll_UNK_UNK_MD_realtime-model_PID.123554558&itm_medium=CPC&itm_source=tiki-reco&spid=123554558"
	tiki = Tiki(base_url='https://tiki.vn/api/v2/', client=uplink.AiohttpClient())
	product = await tiki.get_product_by_url(url)
	assert len(product.ratings) > 0
	LOGGER.info(f"Tiki Product: {product}")
