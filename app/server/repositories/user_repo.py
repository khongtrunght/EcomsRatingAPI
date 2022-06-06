from fastapi import Depends

from server.config.db_old import database

users_ref = database.users


async def create(user: dict):
    user['username'] = user['username'].lower()
    users_ref.insert_one(user)
    return user


async def find_by_username(username: str):
    result = await users_ref.find_one({'username': username})
    return result


