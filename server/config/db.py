from typing import List, Dict

import mongoengine
from mongoengine import Q

from server.models.product import Product
from server.models.reviews import Review

mongoengine.connect(alias='SE_DB',
                    host='mongodb://localhost:27017/RatingDB')


def insert_one_product(name: str, source: str = None, item_id: str = None, shop_id: str = None, reviews: List = [],
                       available: bool = True, num_query: int = 0):  # insert a single product into the DB

    # reviews is a list of reviews, each is a dictionary {rating: float, comment_text: string, images: list(str),
    # videos: list(str)}

    assert name is not None or len(name) == 0, "Name cannot be None or empty"
    new_reviews = []
    for i in range(len(reviews)):
        current_review = reviews[i]
        review = Review()
        review.rating = current_review['rating']
        review.comment_text = current_review['comment_text']
        review.images.extend(current_review['images'])
        review.videos.extend(current_review['videos'])
        new_reviews.append(review)
    new_product = Product()
    new_product.name = name
    new_product.source = source
    new_product.item_id = item_id
    new_product.shop_id = shop_id
    new_product.reviews.extend(new_reviews)
    new_product.available = available
    new_product.query_times = num_query

    new_product.save()


def insert_many_products(products: List[Dict]):  # insert a list of products

    assert len(products) > 0, "products list cannot be empty"
    for p in products:
        name = p['name']
        source = p['source']
        item_id = p['item_id']
        shop_id = p['shop_id']
        reviews = p['reviews']

        in_DB = check_in_DB(item_id, shop_id, source)
        if not in_DB:  # if product p is not in the DB
            insert_one_product(name, source, item_id, shop_id, reviews)  # insert it
        else:  # if it is in the DB already
            query_times = delete_product_by_ids(item_id, shop_id, source)
            insert_one_product(name, shop_id, item_id, shop_id, reviews, num_query=query_times)


def check_in_DB(item_id: str = None, shop_id: str = None, source: str = None) -> bool:
    # check if a product with given set of ids is already in the DB or not

    assert source in ['tiki', 'lazada', 'shoppee'], "Only support either tiki, lazada, or shoppee"
    assert item_id is not None and source is not None, "At least one of item_id or source must be not None"

    results = Product.objects(
        Q(source__iexact=source) & Q(item_id__iexact=item_id) & Q(shop_id__iexact=shop_id))
    results = list(results)
    return len(results) != 0


def search_product_by_name(name: str) -> List[Product]:  # search the products by name
    assert name is not None and len(name) != 0, "Name cannot be None or empty"
    results = Product.objects(name__icontains=name)
    results = list(results)
    if len(results) == 0:  # there is no product with matching name
        insert_one_product(name=name, available=False, num_query=1)
        print("This product is not available")
        return
    outputs = []
    for p in results:
        if p.available:
            outputs.append(p)
        p.query_times += 1
    return outputs


def search_product_by_ids(name: str, item_id: str, shop_id: str, source: str) -> List[Product]:
    # search products by item_id and shop_id
    assert source in ['tiki', 'lazada', 'shoppee'], "Only support either tiki, lazada, or shoppee"
    assert item_id is not None and source is not None, "At least one of item_id or source must be not None"

    results = Product.objects(
        Q(source__iexact=source) & Q(item_id__iexact=item_id) & Q(shop_id__iexact=shop_id))
    results = list(results)
    if len(results) == 0:  # there is no product with matching name
        insert_one_product(name=name, avaiable=False, num_query=1)
        print("This product is not available")
        return
    outputs = []
    for p in results:
        if p.available:
            outputs.append(p)
        p.query_times += 1
    return outputs


def delete_product_by_name(name: str, mode='exact'):  # delete all products with a given name from the DB
    assert name is not None or len(name) == 0, "Name cannot be None or empty"
    assert mode in ['exact', 'contain'], "Mode not supported"
    query = Product.objects(name__exact=name) if mode == 'exact' else Product.objects(name__contains=name)
    query.delete()


def delete_product_by_ids(item_id: str, shop_id: str, source: str):  # delete all prodcust with a given set of ids
    query = Product.objects(
        Q(source__iexact=source) & Q(item_id__iexact=item_id) & Q(shop_id__iexact=shop_id)).first()
    query_times = query.query_times
    query.delete()
    return query_times


def delete_all_product():
    query = Product.objects.all()
    query.delete()
