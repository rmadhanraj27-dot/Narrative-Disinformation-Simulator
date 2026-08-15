from typing import Optional

from app.database.mongodb import database


async def find_matching_event(
    text: str,
    location: Optional[str] = None
):
    """
    Find an existing event that is likely related
    to the social-media post.

    Current version uses simple keyword matching.
    Later this can be replaced with NLP/embedding
    based similarity.
    """

    # ========================================================
    # CLEAN TEXT
    # ========================================================

    words = [
        word.strip(".,!?;:()[]{}\"'")
        for word in text.lower().split()
    ]

    words = [
        word
        for word in words
        if len(word) >= 4
    ]

    if not words:
        return None

    # ========================================================
    # BUILD SEARCH CONDITIONS
    # ========================================================

    conditions = []

    for word in words[:10]:

        conditions.append(
            {
                "$or": [
                    {
                        "title": {
                            "$regex": word,
                            "$options": "i"
                        }
                    },
                    {
                        "description": {
                            "$regex": word,
                            "$options": "i"
                        }
                    }
                ]
            }
        )

    # ========================================================
    # LOCATION FILTER
    # ========================================================

    query = {
        "$and": conditions
    }

    if location:
        query = {
            "$and": [
                {
                    "location": {
                        "$regex": location,
                        "$options": "i"
                    }
                },
                *conditions
            ]
        }

    # ========================================================
    # FIND EVENT
    # ========================================================

    event = await database.events.find_one(
        query
    )

    return event


# ============================================================
# LINK SOCIAL POST TO EVENT
# ============================================================

async def correlate_social_post_with_event(
    post_id: str,
    platform: str = "x",
    location: Optional[str] = None
):
    """
    Find the social post and associate it with
    a matching event.
    """

    # ========================================================
    # FIND SOCIAL POST
    # ========================================================

    post = await database.social_posts.find_one(
        {
            "platform": platform,
            "post_id": post_id
        }
    )

    if post is None:

        return {
            "status": "post_not_found",
            "post": None,
            "event": None
        }

    # ========================================================
    # ALREADY CORRELATED
    # ========================================================

    if post.get("event_id"):

        event = await database.events.find_one(
            {
                "_id": post["event_id"]
            }
        )

        return {
            "status": "already_correlated",
            "post": post,
            "event": event
        }

    # ========================================================
    # FIND MATCHING EVENT
    # ========================================================

    event = await find_matching_event(
        text=post["text"],
        location=location
    )

    if event is None:

        return {
            "status": "no_matching_event",
            "post": post,
            "event": None
        }

    # ========================================================
    # UPDATE SOCIAL POST
    # ========================================================

    await database.social_posts.update_one(
        {
            "_id": post["_id"]
        },
        {
            "$set": {
                "event_id": str(event["_id"])
            }
        }
    )

    # ========================================================
    # GET UPDATED POST
    # ========================================================

    updated_post = await database.social_posts.find_one(
        {
            "_id": post["_id"]
        }
    )

    return {
        "status": "correlated",
        "post": updated_post,
        "event": event
    }