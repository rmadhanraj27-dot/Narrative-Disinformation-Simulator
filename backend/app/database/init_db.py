from app.database.mongodb import database


async def initialize_database():
    collections = await database.list_collection_names()

    required_collections = [
        "users",
        "news",
        "events",
        "narratives",
        "translated_narratives",
        "evolved_narratives",
        "risk_scores",
        "predictions",
        "alerts",
        "activity_logs"
    ]

    for collection_name in required_collections:
        if collection_name not in collections:
            await database.create_collection(collection_name)

    print("MongoDB collections initialized successfully.")