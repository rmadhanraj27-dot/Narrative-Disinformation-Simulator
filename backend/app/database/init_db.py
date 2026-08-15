from app.database.mongodb import database


async def initialize_database():

    collections = await database.list_collection_names()

    required_collections = [
        "users",
        "news",
        "events",
        "social_posts",
        "narratives",
        "translated_narratives",
        "evolved_narratives",
        "risk_scores",
        "predictions",
        "alerts",
        "activity_logs"
    ]

    # ========================================================
    # CREATE REQUIRED COLLECTIONS
    # ========================================================

    for collection_name in required_collections:

        if collection_name not in collections:

            await database.create_collection(
                collection_name
            )

    # ========================================================
    # EVENT INDEXES
    # ========================================================

    await database.events.create_index(
        [
            ("title", 1),
            ("event_type", 1),
            ("location", 1)
        ],
        name="event_duplicate_lookup"
    )

    await database.events.create_index(
        [
            ("source_url", 1)
        ],
        name="event_source_url_lookup",
        sparse=True
    )

    # ========================================================
    # SOCIAL POST INDEXES
    # ========================================================

    await database.social_posts.create_index(
        [
            ("platform", 1),
            ("post_id", 1)
        ],
        name="social_post_unique_id",
        unique=True
    )

    await database.social_posts.create_index(
        [
            ("event_id", 1)
        ],
        name="social_post_event_lookup",
        sparse=True
    )

    await database.social_posts.create_index(
        [
            ("published_at", -1)
        ],
        name="social_post_published_at"
    )

    print(
        "MongoDB collections and indexes initialized successfully."
    )