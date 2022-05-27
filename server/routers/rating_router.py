from fastapi import APIRouter, HTTPException

from server.config.db import fetch_all_ratings, fetch_one_rating, create_rating
from server.schemas.rating import Rating

router = APIRouter(tags=["rating"])


@router.get("/")
async def get_all_ratings():
    rsp = await fetch_all_ratings()
    return rsp


@router.get("/{id}", response_model=Rating)  #
async def get_rating(id):
    rsp = await fetch_one_rating(id)
    if rsp:
        return rsp
    raise HTTPException(404, "There is no rating with id {}".format(id))


@router.post("/", response_model=Rating)
async def post_rating(rating: Rating):
    rsp = await create_rating(rating.dict())
    if rsp:
        return rsp
    raise HTTPException(400, "Failed to create rating")
