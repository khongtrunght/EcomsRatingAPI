import re

from uplink import Consumer, get, QueryMap, returns
from urllib.parse import unquote
import requests
from server.schemas.rating import ShopeeSeachResponse, Rating, ShopeeItem, ShopeeItemInfo

Shopee_url = 'https://shopee.vn'
keyword_search = 'electrical device'


# headers = {'User-Agent': 'Chrome',
#            'Referer': '{}/search?keyword={}'.format(Shopee_url, keyword_search)
#            }


class Shopee(Consumer):
    URL_STR_RE = r"http[s]?://shopee.vn\/(.*)-i\.(\d+)\.(\d+).*"  # 1 ten 2 shopid 3 itemid
    item = "ShopeeItem"

    @returns.from_json(type = ShopeeSeachResponse)
    @get("search/search_items")
    def search_product_by_keyword(self, **options: QueryMap):
        pass

    @get("item/get_ratings")
    def get_rating_list_in(self,
                           **options: QueryMap):  # -> ShopeeRatingResponse:   #itemid, shopid, filter, flag, limit, offset
        pass

    async def get_rating_list(self, **options: QueryMap):
        rsp = await self.get_rating_list_in(**options)
        data = await rsp.json()
        if data['data']['ratings'] is None or len(data['data']['ratings']) == 0:
            return []
        else:
            return [Rating.parse_obj(item) for item in data['data']['ratings']]

    @staticmethod
    def get_convert_products(keyword, limit):
        return dict(keyword = keyword, limit = limit)

    @staticmethod
    def get_convert_ratings(itemid, shopid, offset, limit):
        return dict(itemid = itemid, shopid = shopid, offset = offset, limit = limit)

    async def get_product_by_url(self, url):
        match = re.match(self.URL_STR_RE, url)
        if match:
            name = match.group(1).replace('-', ' ')
            name = unquote(name)
            shopid = match.group(2)
            itemid = match.group(3)

            product = ShopeeItem(item_basic = ShopeeItemInfo(name = name, shopid = shopid, itemid = itemid))
            request = dict(shopid = shopid, itemid = itemid, offset = 0, limit = 5)
            rating_list = await self.get_rating_list(**request)
            product.ratings = rating_list
            return product

# url = 'https://tiki.vn/api/v2/products?limit={}&include=advertisement&aggregations=2&trackity_id=dbda744c-724c-2c2b-b5e7-1842471a03d6&q={}'.format(


# ratings_url = 'https://tiki.vn/api/v2/reviews?limit={}&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={}&spid={}&product_id={}&seller_id={}'


#
#     def find_reviews_by_url(self, url: str):
#         url = urllib.parse.unquote(url)
#         collections = []
#
#         r = re.search(r"i\.(\d+)\.(\d+)", url)
#         r1 = re.search(r"/(\S+)-i", url)
#         name = r1[1].split('/')[2].replace('-', ' ')
#         shopid, itemid = r[1], r[2]
#         print('name = ', name, 'shopid = ', shopid, 'itemid = ', itemid)
#         review = self.get_reviews_list(shopid, itemid)
#         collections.append({'name': name, 'item_id': itemid, 'shop_id': shopid, 'reviews': review, 'source': 'shoppee'})
#
#         return collections
#
