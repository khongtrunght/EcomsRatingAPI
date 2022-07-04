import asyncio
import re

import uplink

from server.crawler.Shopee import Shopee
from server.crawler.Tiki import Tiki
from server.schemas import rating


LIMIT_REVIERW_PER_PRODUCT = 5

class EcomProcess:
	def __init__(self, ecom):
		self.ecom = ecom

	async def get_product(self, url):
		return await self.ecom.get_product_by_url(url)

	async def get_products_list(self, keyword, limit):
		request = self.ecom.get_convert_products(keyword, limit)
		rsp = await self.ecom.search_product_by_keyword(**request)
		return rsp.items

	async def get_ratings_for_product_part(self, itemid, shopid, offset, limit):
		request = self.ecom.get_convert_ratings(itemid, shopid, offset, limit)
		rsp = await self.ecom.get_rating_list(**request)
		# print(rsp)
		return rsp

	async def get_ratings_for_product(self, itemid, shopid):
		sem = asyncio.Semaphore(10)
		output = []

		async def safe_fetch(offset, limit):
			async with sem:
				list_ratings = await self.get_ratings_for_product_part(itemid=itemid, shopid=shopid, offset=offset,
																	   limit=limit)
				output.extend(list_ratings)
		tasks = [asyncio.ensure_future(safe_fetch(offset=0, limit=LIMIT_REVIERW_PER_PRODUCT))]
		# tasks = [asyncio.ensure_future(safe_fetch(offset, limit=LIMIT_REVIERW_PER_PRODUCT)) for offset in range(0, 301, LIMIT_REVIERW_PER_PRODUCT)]
		await asyncio.gather(*tasks)
		return output

	@property
	def regex(self):
		return re.compile(self.ecom.URL_STR_RE)


class Ecom:
	def __init__(self):
		self.ecoms_sys = {'shopee': Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient()),
						  'tiki': Tiki(base_url='https://tiki.vn/api/v2/', client=uplink.AiohttpClient())}

		self.process = {'shopee': EcomProcess(self.ecoms_sys['shopee']),
						'tiki': EcomProcess(self.ecoms_sys['tiki'])}

	async def search_product_by_keyword(self, keyword: str, limit: int = 10):
		list_products = []
		for ecom in self.process.values():
			results = await ecom.get_products_list(keyword=keyword, limit=limit)
			for id, product in enumerate(results):
				rating_list = await ecom.get_ratings_for_product(itemid=product.itemid, shopid=product.shopid)
				results[id].ratings = rating_list
			list_products.extend(results)
		return list_products

	async def search_product_by_url(self, url: str):
		url_re = re.search("http[s]?://([a-z]+).vn.*", url)
		if url_re:
			for ecom_name, ecom in self.process.items():
				if ecom.regex.match(url):
					return await ecom.get_product(url=url)
