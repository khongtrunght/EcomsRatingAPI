import requests
import pandas as pd
import json
import re
import urllib
from typing import overload, Dict
from pythonlangutil.overload import Overload, signature

Tiki_url = 'https://tiki.vn/'
keyword_search = 'electrical device'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
    'Referer': '{}/search?q={}'.format(Tiki_url, keyword_search)
    }


class Tiki:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def search_product_by_keyword(keyword: str, limit: int = 10):
        print("Searching for {} in Tiki ...".format(keyword))
        url = 'https://tiki.vn/api/v2/products?limit={}&include=advertisement&aggregations=2&trackity_id=dbda744c-724c-2c2b-b5e7-1842471a03d6&q={}'.format(
            limit, keyword)

        # Tiki API request
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            print('Cannot request url!!!')
            return []
        r = response.json()

        products = []
        for item in r["data"]:
            name = item["name"]
            shopid = str(item["seller_id"])
            itemid = str(item["id"])
            seller_product_id = str(item["seller_product_id"])
            products.append({'itemid': itemid, 'name': name, 'shopid': shopid, 'spid': seller_product_id})
        return products

    @Overload
    @signature("str", "str", "str", "int")
    def get_reviews_list(self, shopid: str, itemid: str, spid: str, limit: int = 50):
        ratings_url = 'https://tiki.vn/api/v2/reviews?limit={}&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={}&spid={}&product_id={}&seller_id={}'
        offset = 1
        res = []

        while True:
            data = requests.get(ratings_url.format(limit, offset, spid, itemid, shopid), headers=headers).json()
            print(ratings_url.format(limit, offset, spid, itemid, shopid))
            print('data size = ', len(data["data"]))
            i = 1
            for i, rating in enumerate(data["data"], 1):
                # d["username"].append(rating["created_by"]["name"])
                stars = int(rating["rating"])
                comment = rating["content"]
                images = []
                if rating["images"] is not None:
                    images = [img["full_path"] for img in rating["images"]]
                res.append({'rating': stars, 'comment_text': comment, 'images': images, 'videos': []})

                print(rating["created_by"]["name"])
                print(rating["rating"])
                print(rating["content"])
                print("-" * 100)

            if i % limit or len(data["data"]) == 0:
                break
            offset += 1
        return res

    @get_reviews_list.overload
    @signature("str", "int")
    def get_reviews_list(self, itemid: str, limit: int = 50):
        offset = 1
        ratings_url = 'https://tiki.vn/api/v2/reviews?limit={}&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={}&product_id={}'
        res = []
        seller_id = ''

        while True:
            if requests.get(ratings_url.format(limit, offset, itemid), headers=headers).status_code == 403:
                print('url = ', ratings_url.format(limit, offset, itemid))
                print('Cannot request!')
            data = requests.get(ratings_url.format(limit, offset, itemid), headers=headers).json()
            print(ratings_url.format(limit, offset, itemid))
            print('data size = ', len(data["data"]))
            i = 1
            for i, rating in enumerate(data["data"], 1):
                print('i = {}, page = {}'.format(i, offset))
                print('rating = ', 'seller' in rating.keys())
                if 'seller' in rating.keys():
                    seller_id = rating["seller"]["id"]
                stars = int(rating["rating"])
                comment = rating["content"]
                images = []
                if rating["images"] is not None:
                    images = [img["full_path"] for img in rating["images"]]
                res.append({'rating': stars, 'comment_text': comment, 'images': images, 'videos': []})

                print(rating["created_by"]["name"])
                print(rating["rating"])
                print(rating["content"])
                print("-" * 100)

            if i % limit or len(data["data"]) == 0:
                break
            offset += 1
        return res, str(seller_id)

    def find_reviews_by_keyword(self, keyword: str, search_limit: int = 10, review_limit: int = 50):
        print("Collecting reviews related to {} ...".format(keyword))
        product_lists = self.search_product_by_keyword(keyword, search_limit)
        collections = []
        for product in product_lists:
            name = product["name"]
            shopid = str(product["shopid"])
            itemid = str(product["itemid"])
            spid = str(product["spid"])
            review = self.get_reviews_list(shopid, itemid, spid, review_limit)
            collections.append(
                {'item_id': str(itemid), 'name': name, 'shop_id': str(shopid), 'reviews': review, 'source': 'tiki'})
        return collections

    def find_reviews_by_url(self, url: str, limit: int = 20):
        url = urllib.parse.unquote(url)
        collections = []
        r = re.search(r"p(\d+).", url)
        r1 = re.search(r"/(\S+)-", url)
        name = r1[0].split('/')[3].replace('-', ' ')
        itemid = r[0][1:-1]
        review, shopid = self.get_reviews_list(itemid, limit)
        collections.append({'item_id': itemid, 'name': name, 'shop_id': shopid, 'reviews': review, 'source': 'tiki'})

        return collections


if __name__ == '__main__':
    tiki = Tiki(Tiki_url)
    keyword = 'electrical device'
    # url = 'https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=2&trackity_id=dbda744c-724c-2c2b-b5e7-1842471a03d6&q={}'.format(keyword)

    spid = 65556526
    itemid = 65556522
    shopid = 67471
    # res = tiki.get_reviews_list('162772687')
    ratings_url = f'https://tiki.vn/api/v2/reviews?limit=5&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page=1&spid={spid}&product_id={itemid}&seller_id={shopid}'
    url = f'https://tiki.vn/api/v2/reviews?product_id={itemid}&include=comments&page=1&limit=-1&top=true&spid={spid}&seller_id={shopid}'
    link = 'https://tiki.vn/chuot-khong-day-multi-device-dell-ms5320w-hang-chinh-hang-p57866963.html?spid=117573048'
    res = tiki.find_reviews_by_keyword('heat shrink tube tubing kit tool black shrinkage set safely protect electrical')
    # res = tiki.find_reviews_by_url('https://tiki.vn/chuot-van-phong-khong-day-cao-cap-imice-g-6-silent-2-4g-wireles-6-nut-dieu-khien-ket-noi-nhanh-bo-thu-nano-tu-dong-ket-noi-khoang-cach-lam-viec-10m-tiet-kiem-pin-thong-minh-do-phan-giai-800-1200-1600dpi-hang-chinh-hang-p101284469.html?itm_campaign=HMP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.38799_Y.393264_Z.920872_CN.TONG-HOP-1&itm_medium=CPC&itm_source=tiki-ads&spid=101284475')
    filename = 'tiki_test.json'

    # with open(filename, 'w', encoding='utf8') as file_object:  #open the file in write mode
    #  json.dump(res, file_object, ensure_ascii=False)
    print(json.dumps(res, indent=2))
    print(pd.DataFrame(res))
