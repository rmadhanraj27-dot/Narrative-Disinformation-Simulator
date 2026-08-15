from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings


# ============================================================
# MONGODB CONNECTION
# ============================================================

client = AsyncIOMotorClient(
    settings.mongo_uri
)

database = client[
    settings.database_name
]


# ============================================================
# CHECK DATABASE CONNECTION
# ============================================================

async def check_database_connection():

    try:
        await client.admin.command("ping")
        return True

    except Exception as error:
        print(f"MongoDB connection error: {error}")
        return False


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

async def close_database_connection():

    client.close()

    print("MongoDB connection closed.")