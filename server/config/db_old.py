import motor.motor_asyncio
from server.schemas.rating import Rating

conn = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = conn.RatingDB


# collection like table
collection = database.rating


async def fetch_one_rating(id):
    document = await collection.find_one({"_id": id})
    return Rating(**document)


async def fetch_all_ratings():
    ratings = []
    cursor = collection.find({})
    async for document in cursor:
        ratings.append(Rating(**document))
    return ratings


async def create_rating(rating):
    document = rating
    result = await collection.insert_one(document)
    return document
