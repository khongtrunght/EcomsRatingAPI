import uplink
import pytest
from server.crawler.Ecom import Ecom
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
NUM_OF_ECOM = 2

@pytest.mark.asyncio
async def test_get_list_products():
	crawler = Ecom()
	rsp = await crawler.search_product_by_keyword(keyword='áo', limit=10)
	assert len(rsp) == 10 * NUM_OF_ECOM
	LOGGER.info(rsp)


@pytest.mark.asyncio
async def test_search_product_by_url():
	crawler = Ecom()
	url = "https://shopee.vn/Qu%E1%BA%A7n-%E1%BB%91ng-su%C3%B4ng-r%E1%BB%99ng-n%E1%BB%AF-culottes-kho%CC%81a-tr%C6%B0" \
		  "%C6%A1%CC%81c-va%CC%89i-m%E1%BB%81m-nhi%C3%AA%CC%80u-ma%CC%80u-i.66764726.4913616968?sp_atk=e3ade505-d481" \
		  "-4685-96e2-4fe618a166e9&xptdk=e3ade505-d481-4685-96e2-4fe618a166e9 "
	rsp = await crawler.search_product_by_url(url=url)
	assert len(rsp.ratings) > 0
	LOGGER.info(rsp)
