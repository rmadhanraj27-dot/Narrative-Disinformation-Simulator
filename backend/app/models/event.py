from datetime import datetime, timezone


def create_event_document(
    title: str,
    description: str,
    event_type: str,
    location: str | None,
    language: str,
    source: str,
    source_url: str | None,
    severity: str
):
    """
    Creates the MongoDB document for an event.
    """

    current_time = datetime.now(timezone.utc)

    return {
        "title": title,
        "description": description,
        "event_type": event_type,
        "location": location,
        "language": language,
        "source": source,
        "source_url": source_url,
        "severity": severity,
        "created_at": current_time,
        "updated_at": current_time
    }


def event_response(event: dict):
    """
    Converts a MongoDB event document
    into a JSON-friendly response.
    """

    return {
        "id": str(event["_id"]),
        "title": event["title"],
        "description": event["description"],
        "event_type": event["event_type"],
        "location": event.get("location"),
        "language": event["language"],
        "source": event["source"],
        "source_url": event.get("source_url"),
        "severity": event["severity"],
        "created_at": event["created_at"],
        "updated_at": event["updated_at"]
    }