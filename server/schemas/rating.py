from typing import List
from datetime import date

from pydantic import BaseModel, conint
from pydantic.types import constr


class Rating(BaseModel):
    # orderid: int
    # itemid: int
    # cmtid: int
    # ctime: int
    comment_text : str
    # rating is int in range 1 to 5
    # rating: conint(ge=1, le=5) = 2
    images: List[str]
    rating : int
    videos : List[str]


class Product(BaseModel):
    name: str
    item_id: str
    shop_id: str
    source: str
    # date: int
    query_times: int
    reviews: List[Rating]
    available: bool


class DoByRequest(BaseModel):
    input_data: str
    by: constr(regex='^(keyword|url)$') = 'keyword'
