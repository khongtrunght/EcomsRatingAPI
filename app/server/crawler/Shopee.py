import asyncio
from collections import defaultdict
from typing import List

import requests
import pandas as pd
import json
import re
import urllib

import uplink
from uplink import Consumer, get, Query, QueryMap, returns, headers, json
from server.schemas.rating import ShopeeSeachResponse, ShopeeItem, ShopeeRatingResponse, TikiSearchResponse, \
    TikiRatingResponse, Rating
from abc import abstractmethod

Shopee_url = 'https://shopee.vn'
keyword_search = 'electrical device'
# headers = {'User-Agent': 'Chrome',
#            'Referer': '{}/search?keyword={}'.format(Shopee_url, keyword_search)
#            }


class Shopee(Consumer):
    @get("search/search_items")
    def search_product_by_keyword(self, **options: QueryMap) -> ShopeeSeachResponse:
        pass

    @get("item/get_ratings")
    def get_rating_list_in(self, **options: QueryMap )  : # -> ShopeeRatingResponse:   #itemid, shopid, filter, flag, limit, offset
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
        return dict(keyword=keyword, limit=limit)

    @staticmethod
    def get_convert_ratings(itemid, shopid, offset, limit):
        return dict(itemid=itemid, shopid=shopid, offset=offset, limit=limit)


# url = 'https://tiki.vn/api/v2/products?limit={}&include=advertisement&aggregations=2&trackity_id=dbda744c-724c-2c2b-b5e7-1842471a03d6&q={}'.format(


# ratings_url = 'https://tiki.vn/api/v2/reviews?limit={}&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={}&spid={}&product_id={}&seller_id={}'

class Tiki(Consumer):
    @get("products")
    def search_product_by_keyword(self, **options: QueryMap)  -> TikiSearchResponse:   #q, limit, include: str = 'advertisement', aggregations: int = 2,
                                 # trackity_id: str = 'dbda744c-724c-2c2b-b5e7-1842471a03d6'
        pass

    # async def search_product_by_keyword(self, **options: QueryMap):
    #     rsp = await self.search_product_by_keyword_in(**options)
    #     rsp = await rsp.json()
    #     rsp['items'] = rsp['data']
    #     return ShopeeSeachResponse(items=[])


    @get("reviews")
    # @returns.json
    def get_rating_list_in(self, **options: QueryMap) :  #include: str = 'comments,contribute_info', sort: str = 'score|desc,id|desc,stars|all',
                       # page: int = 1, spid: str = '', product_id: str = '', seller_id: str = ''
        pass

    async def get_rating_list(self, **options: QueryMap) :
        data = await self.get_rating_list_in(**options)
        review_list = await data.json()
        review_list = review_list['data']
        output_list = [Rating(rating=review['rating'], comment=review['content'], images=[image['full_path'] for image in review['images']]) for review in review_list]
        return output_list


    @staticmethod
    def get_convert_products(keyword, limit):
        return dict(q=keyword, limit=limit)

    @staticmethod
    def get_convert_ratings(itemid, shopid, offset=0, limit=10):
        return dict(seller_id=shopid, product_id=itemid, offset=offset, limit=limit)


class ShopeeProcess:
    def __init__(self, shopee):
        #Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient())
        self.shopee = shopee

    async def get_products_list(self, keyword, limit) :
        # defaultdict(keyword=keyword, limit=limit)
        request = self.shopee.get_convert_products(keyword, limit)
        rsp = await self.shopee.search_product_by_keyword(**request)
        return rsp.items

    async def get_ratings_for_product_part(self, itemid, shopid, offset, limit):
        request = self.shopee.get_convert_ratings(itemid, shopid, offset, limit)
        rsp = await self.shopee.get_rating_list(**request)
        # print(rsp)
        return rsp

    async def get_ratings_for_product(self, itemid, shopid):
        # rsp = await self.shopee.get_rating_list(itemid=itemid, shopid=shopid, limit=50, offset=0)
        sem = asyncio.Semaphore(10)
        output = []

        async def safe_fetch(offset, limit):
            async with sem:
                list_ratings = await self.get_ratings_for_product_part(itemid=itemid, shopid=shopid, offset=offset, limit=limit)
                output.extend(list_ratings)

        tasks = [asyncio.ensure_future(safe_fetch(offset, limit=50)) for offset in range(0, 301, 50)]
        await asyncio.gather(*tasks)
        return output


class Ecom:
    def __init__(self):
        self.ecoms_sys = {'shopee': Shopee(base_url='https://shopee.vn/api/v4/', client=uplink.AiohttpClient()),
                          'tiki': Tiki(base_url='https://tiki.vn/api/v2/', client=uplink.AiohttpClient())}

        self.process = {'shopee': ShopeeProcess(self.ecoms_sys['shopee']),
                        'tiki': ShopeeProcess(self.ecoms_sys['tiki'])}

    async def search_product_by_keyword(self, keyword: str, limit: int = 10):
        list_products = []
        for ecom in self.process.values():
            results = await ecom.get_products_list(keyword=keyword, limit=limit)
            for id, product in enumerate(results):
                rating_list = await ecom.get_ratings_for_product(itemid=product.itemid, shopid=product.shopid)
                results[id].ratings = rating_list
            list_products.extend(results)
        return list_products




# class Shopee:
#     def __init__(self, url: str):
#         self.url = url
#
#     def search_product_by_keyword(self, keyword: str, limit: str = '20'):
#         print("Searching for {} in shopee ...".format(keyword))
#         products = []
#         url = r'https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(
#             keyword)
#         print('url = ', url)
#         # Shopee API request
#         response = requests.get(url, headers=headers)
#         if requests.get(url, headers=headers).status_code == 403:
#             print('Cannot request url!!!')
#             return []
#         r = response.json()
#         print(json.dumps(r, indent=2))
#         for item in r["items"]:
#             info = item['item_basic']
#             name = info["name"]
#             shopid = str(info["shopid"])
#             itemid = str(info["itemid"])
#             products.append({'itemid': itemid, 'name': name, 'shopid': shopid})
#
#         return products
#
#     def get_reviews_list(self, shopid: str, itemid: str, limit: int = 50, type=0):
#         offset = 0
#         ratings_url = 'https://shopee.vn/api/v4/item/get_ratings?filter=0&flag=1&itemid={}&limit={}&offset={}&shopid={}&type=0'
#         # offset: xem danh gia thu i = offset
#         # limit: tra ve toi da bao nhieu danh gia 1 lan goi
#
#         results = []
#         while True:
#             data = requests.get(ratings_url.format(itemid, limit, offset, shopid)).json()
#             print(ratings_url.format(itemid, limit, offset, shopid))
#             print('data size', len(data["data"]["ratings"]))
#             # print(json.dumps(data, indent=2))
#             i = 1
#             # try:
#             for i, rating in enumerate(data["data"]["ratings"], 1):
#                 # d["username"].append(rating["author_username"])
#                 star = int(rating["rating_star"])
#                 comment_text = rating["comment"]
#                 images = []
#                 videos = []
#                 if rating["images"] is not None:
#                     images = ['https://cf.shopee.vn/file/{}_tn'.format(img) for img in rating["images"]]
#                 print('images = ', images)
#                 if rating["videos"] is not None:
#                     for video in rating["videos"]:
#                         videos.append(video["url"])
#                 results.append({'rating': star, 'comment_text': comment_text, 'images': images, 'videos': videos})
#
#                 print(rating["author_username"])
#                 print(rating["rating_star"])
#                 print(rating["comment"])
#                 print("-" * 100)
#
#             if i % limit or len(data["data"]) == 0:
#                 break
#             offset += limit
#         return results
#
#     def find_reviews_by_keyword(self, keyword: str, limit: int = 20):
#         print("Collecting reviews related to {} ...".format(keyword))
#         product_lists = self.search_product_by_keyword(keyword, int)
#         collections = []
#         for product in product_lists:
#             name = str(product["name"])
#             shopid = str(product["shopid"])
#             itemid = str(product["itemid"])
#             review = self.get_reviews_list(shopid, itemid)
#             collections.append(
#                 {'item_id': itemid, 'name': name, 'shop_id': shopid, 'reviews': review, 'source': 'shoppee'})
#         return collections
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

if __name__ == '__main__':
    new = Shopee(Shopee_url)
    # list = new.search_product_by_keyword(keyword_search)
    # df = pd.DataFrame(list)
    # print(df)  # print only the head for brevity
    # print("-" * 80)

    url = 'https://shopee.vn/D%C3%89P-T%C3%94NG-N%C6%A0-K%E1%BA%BA-CARO-i.7332956.19101749350?sp_atk=08cca8a5-dabe-47ae-bcf5-6b8c3dc93d9d&xptdk=08cca8a5-dabe-47ae-bcf5-6b8c3dc93d9d'
    res = new.find_reviews_by_keyword('heat shrink tube tubing kit tool black shrinkage set safely protect electrical')
    # res = new.find_reviews_by_keyword('chuot-khong-day-multi-device-dell-ms5320w')
    # res = new.find_reviews_by_url(url)
    print(res)
    print(json.dumps(res, indent=2))
    print(pd.DataFrame(res))

    # filename = 'shopee.json'
    # with open(filename, 'w', encoding='utf8') as file_object:  #open the file in write mode
    #  json.dump(r, file_object, ensure_ascii=False)
