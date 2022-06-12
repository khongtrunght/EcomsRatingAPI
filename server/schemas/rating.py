from typing import List
from datetime import date

from pydantic import BaseModel, conint
from pydantic.types import constr


class Rating(BaseModel):
    rating: conint(ge=0, le=5) = 2
    comment_text: str
    images: List[str]
    videos: List[str]


class Product(BaseModel):
    name: str
    item_id: str
    shop_id: str
    source: str
    query_times: int
    reviews: List[Rating]
    available: bool
    avg_rating: float = 0.0

class ID(BaseModel):
    source: str
    item_id: str
    shop_id: str

class DoByRequest(BaseModel):
    input_data: str
    by: constr(regex='^(keyword|url)$') = 'keyword'


