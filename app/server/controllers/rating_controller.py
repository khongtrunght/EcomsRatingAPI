import server.repositories.rating_repo as rating_repo
from server.schemas.rating import Product


async def search_product_by(data, by):
    products = None
    if by == 'keyword':
        products = await rating_repo.search_product_by_keyword(data)
    elif by == 'url':
        products = await rating_repo.search_product_by_url(data)

    products_list = [Product(**product) for product in products]

    rsp = {
        'message': f'search by {by} success. Return {len(products_list)} products',
        'status_code': 200,
        'data': products_list,
    }

    return rsp
