import requests
import pandas as pd
import json
import re

from uplink import Consumer, get, QueryMap
from urllib.parse import unquote

from server.schemas.rating import TikiSearchResponse, Rating, TikiItem

Tiki_url = 'https://tiki.vn/'
keyword_search = 'electrical device'
headers = {
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
	'Referer': '{}/search?q={}'.format(Tiki_url, keyword_search)
}

# http[s]?:\/\/[a-z]+.vn\/.+i\.(\d+)\.(\d+).*

# -p(\d+).
# def find_reviews_by_url(self, url: str, limit: int = 20):
#     url = urllib.parse.unquote(url)
#     collections = []
#     r = re.search(r"p(\d+).", url)
#     r1 = re.search(r"/(\S+)-", url)
#     name = r1[0].split('/')[3].replace('-', ' ')
#     itemid = r[0][1:-1]
#     review, shopid = self.get_reviews_list(itemid, limit)
#     collections.append({'item_id': itemid, 'name': name, 'shop_id': shopid, 'reviews': review, 'source': 'tiki'})
#
#     return collections


class Tiki(Consumer):
	URL_STR_RE = "http[s]?://tiki.vn/(.*)-.*-p(\d+)..*" #http[s]?://([a-z]+).vn/(.*)-.*-p(\d+)..*
	item = "TikiItem"

	@get("products")
	def search_product_by_keyword(self,
								  **options: QueryMap) -> TikiSearchResponse:  # q, limit, include: str = 'advertisement', aggregations: int = 2,
		# trackity_id: str = 'dbda744c-724c-2c2b-b5e7-1842471a03d6'
		pass

	@get("reviews")
	# @returns.json
	def get_rating_list_in(self,
						   **options: QueryMap):  # include: str = 'comments,contribute_info', sort: str = 'score|desc,id|desc,stars|all',
		# page: int = 1, spid: str = '', product_id: str = '', seller_id: str = ''
		pass

	async def get_rating_list(self, **options: QueryMap):
		data = await self.get_rating_list_in(**options)
		review_list = await data.json()
		review_list = review_list['data']
		output_list = [Rating(rating=review['rating'], comment=review['content'],
							  images=[image['full_path'] for image in review['images']]) for review in review_list]
		return output_list

	@staticmethod
	def get_convert_products(keyword, limit):
		return dict(q=keyword, limit=limit)

	@staticmethod
	def get_convert_ratings(itemid, shopid, offset=0, limit=5):
		return dict(seller_id=shopid, product_id=itemid, offset=offset, limit=limit)

	async def get_product_by_url(self, url):
		match = re.match(self.URL_STR_RE, url)
		if match:
			name = match.group(1).replace('-', ' ')
			name = unquote(name)
			shopid = 0
			itemid = match.group(2)

			product = TikiItem(name=name, shopid=shopid, itemid=itemid)
			request = self.get_convert_ratings(itemid, shopid)
			rating_list = await self.get_rating_list(**request)
			product.ratings = rating_list
			return product
