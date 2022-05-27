from typing import List

from pydantic import BaseModel, conint


class Rating(BaseModel):
    orderid: int
    itemid: int
    cmtid: int
    ctime: int
    # rating is int in range 1 to 5
    rating_star: conint(ge=1, le=5)
    images: List[str]
