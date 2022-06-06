from fastapi import APIRouter

from server.config.db_old import conn

user = APIRouter()


@user.get("/")
async def find_all_users():
    return conn.local.user.find()