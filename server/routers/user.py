from fastapi import APIRouter

from server.config.db import conn

user = APIRouter()


@user.get("/")
async def find_all_users():
    return conn.local.user.find()