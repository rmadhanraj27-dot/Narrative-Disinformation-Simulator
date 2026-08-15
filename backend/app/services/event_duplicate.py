from typing import Optional

from app.database.mongodb import database


async def find_duplicate_event(
    title: str,
    event_type: str,
    location: Optional[str] = None,
    source_url: Optional[str] = None
):
    """
    Check whether an event already exists.

    Priority:
    1. Exact source URL
    2. Title + event type + location
    """

    # ========================================================
    # CHECK 1 — SOURCE URL
    # ========================================================

    if source_url:

        existing_event = await database.events.find_one(
            {
                "source_url": source_url
            }
        )

        if existing_event is not None:

            return existing_event


    # ========================================================
    # CHECK 2 — TITLE + EVENT TYPE + LOCATION
    # ========================================================

    query = {
        "title": title,
        "event_type": event_type,
        "location": location
    }

    existing_event = await database.events.find_one(
        query
    )

    return existing_event