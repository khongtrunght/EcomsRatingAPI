import app.server.repositories.rating_repo as rating_repo
from server.schemas.rating import Product


def search_product_by(data, by):
    products = None
    if by == 'keyword':
        products = rating_repo.search_product_by_keyword(data)
    elif by == 'url':
        products = rating_repo.search_product_by_url(data)

    rsp = [Product(**product) for product in products]

    return rsp
