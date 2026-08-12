import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()


MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "narrative_disinformation_db"
)


client = AsyncIOMotorClient(MONGO_URI)

database = client[DATABASE_NAME]


async def check_database_connection():
    try:
        await client.admin.command("ping")
        return True
    except Exception as error:
        print(f"MongoDB connection error: {error}")
        return False


async def close_database_connection():
    client.close()