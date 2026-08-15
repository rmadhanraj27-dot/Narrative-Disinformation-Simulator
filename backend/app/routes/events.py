from bson import ObjectId

from fastapi import APIRouter, HTTPException, status

from app.database.mongodb import database

from app.models.event import (
    create_event_document,
    event_response
)

from app.schemas.event import EventCreate

from app.services.event_duplicate import (
    find_duplicate_event
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# ============================================================
# CREATE EVENT
# ============================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_event(event: EventCreate):

    try:

        # ====================================================
        # CHECK FOR DUPLICATE EVENT
        # ====================================================

        existing_event = await find_duplicate_event(
            title=event.title,
            event_type=event.event_type,
            location=event.location,
            source_url=event.source_url
        )

        if existing_event is not None:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A similar event already exists"
            )

        # ====================================================
        # CREATE EVENT DOCUMENT
        # ====================================================

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

        # ====================================================
        # INSERT INTO MONGODB
        # ====================================================

        result = await database.events.insert_one(
            event_document
        )

        # ====================================================
        # GET CREATED EVENT
        # ====================================================

        created_event = await database.events.find_one(
            {
                "_id": result.inserted_id
            }
        )

        if created_event is None:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Event could not be retrieved after creation"
            )

        return {
            "message": "Event created successfully",
            "event": event_response(created_event)
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"Error creating event: {error}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event"
        )


# ============================================================
# GET ALL EVENTS
# ============================================================

@router.get("")
async def get_events():

    try:

        cursor = database.events.find(
            {}
        ).sort(
            "created_at",
            -1
        )

        events = []

        async for event in cursor:

            events.append(
                event_response(event)
            )

        return {
            "count": len(events),
            "events": events
        }

    except Exception as error:

        print(
            f"Error retrieving events: {error}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve events"
        )


# ============================================================
# GET SINGLE EVENT
# ============================================================

@router.get("/{event_id}")
async def get_event(event_id: str):

    # ========================================================
    # VALIDATE OBJECT ID
    # ========================================================

    if not ObjectId.is_valid(event_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid event ID"
        )

    try:

        event = await database.events.find_one(
            {
                "_id": ObjectId(event_id)
            }
        )

        if event is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return {
            "event": event_response(event)
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"Error retrieving event: {error}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve event"
        )