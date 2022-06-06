import requests
import pandas as pd
import json
import re
import urllib

Shopee_url = 'https://shopee.vn'
keyword_search = 'electrical device'
headers = {'User-Agent': 'Chrome',
           'Referer': '{}/search?keyword={}'.format(Shopee_url, keyword_search)
           }


class Shopee:
    def __init__(self, url: str):
        self.url = url

    def search_product_by_keyword(self, keyword: str, limit: str = '20'):
        print("Searching for {} in shopee ...".format(keyword))
        products = []
        url = r'https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(
            keyword)
        print('url = ', url)
        # Shopee API request
        response = requests.get(url, headers=headers)
        if requests.get(url, headers=headers).status_code == 403:
            print('Cannot request url!!!')
            return []
        r = response.json()
        print(json.dumps(r, indent=2))
        for item in r["items"]:
            info = item['item_basic']
            name = info["name"]
            shopid = str(info["shopid"])
            itemid = str(info["itemid"])
            products.append({'itemid': itemid, 'name': name, 'shopid': shopid})

        return products

    def get_reviews_list(self, shopid: str, itemid: str, limit: int = 50):
        offset = 0
        ratings_url = 'https://shopee.vn/api/v4/item/get_ratings?filter=0&flag=1&itemid={}&limit={}&offset={}&shopid={}&type=0'
        # offset: xem danh gia thu i = offset
        # limit: tra ve toi da bao nhieu danh gia 1 lan goi

        results = []
        while True:
            data = requests.get(ratings_url.format(itemid, limit, offset, shopid)).json()
            print(ratings_url.format(itemid, limit, offset, shopid))
            print('data size', len(data["data"]["ratings"]))
            # print(json.dumps(data, indent=2))
            i = 1
            # try:
            for i, rating in enumerate(data["data"]["ratings"], 1):
                # d["username"].append(rating["author_username"])
                star = int(rating["rating_star"])
                comment_text = rating["comment"]
                images = []
                videos = []
                if rating["images"] is not None:
                    images = ['https://cf.shopee.vn/file/{}_tn'.format(img) for img in rating["images"]]
                print('images = ', images)
                if rating["videos"] is not None:
                    for video in rating["videos"]:
                        videos.append(video["url"])
                results.append({'rating': star, 'comment_text': comment_text, 'images': images, 'videos': videos})

                print(rating["author_username"])
                print(rating["rating_star"])
                print(rating["comment"])
                print("-" * 100)

            if i % limit or len(data["data"]) == 0:
                break
            offset += limit
        return results

    def find_reviews_by_keyword(self, keyword: str, limit: int = 20):
        print("Collecting reviews related to {} ...".format(keyword))
        product_lists = self.search_product_by_keyword(keyword, int)
        collections = []
        for product in product_lists:
            name = str(product["name"])
            shopid = str(product["shopid"])
            itemid = str(product["itemid"])
            review = self.get_reviews_list(shopid, itemid)
            collections.append(
                {'item_id': itemid, 'name': name, 'shop_id': shopid, 'reviews': review, 'source': 'shoppee'})
        return collections

    def find_reviews_by_url(self, url: str):
        url = urllib.parse.unquote(url)
        collections = []

        r = re.search(r"i\.(\d+)\.(\d+)", url)
        r1 = re.search(r"/(\S+)-i", url)
        name = r1[1].split('/')[2].replace('-', ' ')
        shopid, itemid = r[1], r[2]
        print('name = ', name, 'shopid = ', shopid, 'itemid = ', itemid)
        review = self.get_reviews_list(shopid, itemid)
        collections.append({'name': name, 'item_id': itemid, 'shop_id': shopid, 'reviews': review, 'source': 'shoppee'})

        return collections


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
