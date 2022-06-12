from typing import List, Union, Optional
from datetime import date
import datetime
from pydantic import BaseModel, conint, Field, validator
from pydantic.schema import Dict
from pydantic.types import constr


class Rating(BaseModel):

    class Config:
        allow_population_by_field_name = True

    rating: float
    # comment_text: str
    comment: str = Field(alias='comment_text')
    images: List = []
    videos: Union[List] = []

    @validator('images', pre=True)
    def check_none(value, field):
        if value is None:
            return []
        return value





class TikiRating(BaseModel):

    class Config:
        allow_population_by_field_name = True

    class TikiImage(BaseModel):
        full_path: str

    content : str = Field(alias='comment')
    rating : conint(ge=0, le=5)
    images : Union[List[Optional[TikiImage]], None] = []







class Product(BaseModel):
    name: str
    item_id: str
    shop_id: str
    source: str
    query_times: int = 0
    reviews: List[Rating]
    available: bool = True
    avg_rating: float = 0.0
    date : datetime.datetime = datetime.datetime.now()

class ID(BaseModel):
    source: str
    item_id: str
    shop_id: str

class DoByRequest(BaseModel):
    input_data: str
    by: constr(regex='^(keyword|url)$') = 'keyword'


class ShopeeItemInfo(BaseModel):
    itemid: int
    shopid: int
    name: str


class ShopeeItem(BaseModel):
    item_basic: ShopeeItemInfo
    ratings: List[Rating] = []
    @property
    def itemid(self):
        return self.item_basic.itemid

    @property
    def shopid(self):
        return self.item_basic.shopid

    @property
    def name(self):
        return self.item_basic.name


class ShopeeSeachResponse(BaseModel):

    items: List[ShopeeItem]


class ShopeeRatingResponse(BaseModel):
    class Ratings(BaseModel):
        ratings: List[Optional[Rating]]

    data: Ratings


class TikiItem(BaseModel):
    name: str
    seller_id: int = Field(alias='shopid')
    id: int = Field(alias ='itemid')
    ratings: List[Rating] = []

    @property
    def itemid(self):
        return self.id

    @property
    def shopid(self):
        return self.seller_id

    class Config:
        allow_population_by_field_name = True


class TikiSearchResponse(BaseModel):
    data : List[TikiItem] = Field(alias='items')

    @property
    def items(self):
        return self.data

    class Config:
        allow_population_by_field_name = True


class TikiRatingResponse(BaseModel):
    data: List[TikiRating]
