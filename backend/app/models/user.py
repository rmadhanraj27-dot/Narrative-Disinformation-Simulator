from datetime import datetime, timezone

from bson import ObjectId


def create_user_document(
    name: str,
    email: str,
    password_hash: str,
):
    return {
        "name": name,
        "email": email.lower().strip(),
        "password_hash": password_hash,
        "preferred_language": "en",
        "notifications_enabled": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


def user_response(user: dict):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "preferred_language": user.get("preferred_language", "en"),
        "notifications_enabled": user.get(
            "notifications_enabled",
            True
        ),
        "created_at": user["created_at"],
    }