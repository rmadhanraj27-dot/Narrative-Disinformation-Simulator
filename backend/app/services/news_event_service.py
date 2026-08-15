from app.database.mongodb import database

from app.schemas.news import NewsArticle

from app.services.news_to_event import news_article_to_event

from app.services.event_duplicate import find_duplicate_event

from app.models.event import (
    create_event_document,
    event_response
)


async def save_news_article_as_event(
    article: NewsArticle
):
    """
    Convert a NewsAPI article into an event,
    check for duplicates, and save it to MongoDB.
    """

    # ========================================================
    # STEP 1 — CONVERT NEWS ARTICLE TO EVENT
    # ========================================================

    event = news_article_to_event(article)

    # ========================================================
    # STEP 2 — CHECK FOR DUPLICATE
    # ========================================================

    existing_event = await find_duplicate_event(
        title=event.title,
        event_type=event.event_type,
        location=event.location,
        source_url=event.source_url
    )

    if existing_event is not None:

        return {
            "status": "already_exists",
            "event": event_response(existing_event)
        }

    # ========================================================
    # STEP 3 — CREATE EVENT DOCUMENT
    # ========================================================

    event_document = create_event_document(
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        location=event.location,
        language=event.language,
        source=event.source,
        source_url=event.source_url,
        severity=event.severity
    )

    # ========================================================
    # STEP 4 — SAVE TO MONGODB
    # ========================================================

    result = await database.events.insert_one(
        event_document
    )

    # ========================================================
    # STEP 5 — RETRIEVE SAVED EVENT
    # ========================================================

    saved_event = await database.events.find_one(
        {
            "_id": result.inserted_id
        }
    )

    if saved_event is None:

        raise RuntimeError(
            "Event was inserted but could not be retrieved"
        )

    return {
        "status": "created",
        "event": event_response(saved_event)
    }