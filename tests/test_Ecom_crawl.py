import uplink
import pytest
from server.crawler.Shopee import Ecom


@pytest.mark.asyncio
async def test_get_list_products():
    crawler = Ecom()
    rsp = await crawler.search_product_by_keyword(keyword='áo', limit=10)
    print(rsp)
