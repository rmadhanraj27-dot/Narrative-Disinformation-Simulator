from app.database.mongodb import database


async def initialize_database():

    # ========================================================
    # CREATE REQUIRED COLLECTIONS
    # ========================================================

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


    # ========================================================
    # USERS INDEX
    # ========================================================

    await database.users.create_index(
        "email",
        unique=True
    )


    # ========================================================
    # EVENTS INDEXES
    # ========================================================

    # Newest events first
    await database.events.create_index(
        [
            ("created_at", -1)
        ]
    )

    # Filter by event type
    await database.events.create_index(
        [
            ("event_type", 1)
        ]
    )

    # Filter by severity
    await database.events.create_index(
        [
            ("severity", 1)
        ]
    )

    # Filter by language
    await database.events.create_index(
        [
            ("language", 1)
        ]
    )

    # Event type + newest events
    await database.events.create_index(
        [
            ("event_type", 1),
            ("created_at", -1)
        ]
    )

    print("MongoDB indexes initialized successfully.")