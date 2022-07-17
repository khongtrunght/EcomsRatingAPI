import server.repositories.rating_repo as rating_repo
from server.schemas.rating import Product


async def search_product_by(data, by, limit):
    products = None
    if by == 'keyword':
        products = await rating_repo.search_product_by_keyword(data, limit)
    elif by == 'url':
        products = await rating_repo.search_product_by_url(data)

    rsp = [Product(**product) for product in products]

    return rsp
