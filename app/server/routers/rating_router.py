from typing import List

from fastapi import APIRouter, HTTPException

from server.schemas.rating import Rating, DoByRequest, Product
import server.controllers.rating_controller as rating_controller

router = APIRouter(tags=["rating"])


# @router.get("/")
# async def get_all_ratings():
#     rsp = await fetch_all_ratings()
#     return rsp
#
#
# @router.get("/{id}", response_model=Rating)  #
# async def get_rating(id):
#     rsp = await fetch_one_rating(id)
#     if rsp:
#         return rsp
#     raise HTTPException(404, "There is no rating with id {}".format(id))
#
#
# @router.post("/", response_model=Rating)
# async def post_rating(rating: Rating):
#     rsp = await create_rating(rating.dict())
#     if rsp:
#         return rsp
#     raise HTTPException(400, "Failed to create rating")


@router.post("/", response_model=List[Product]) # ,
async def get_rating_by(request: DoByRequest):
    rsp = await rating_controller.search_product_by(data=request.input_data, by=request.by, limit = request.limit_per_ecom)
    return rsp

