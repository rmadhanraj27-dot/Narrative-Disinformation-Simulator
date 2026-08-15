from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from app.database.mongodb import database
from app.schemas.social import SocialPost


def serialize_social_post(post):
    """
    Convert MongoDB document into JSON-compatible data.
    """

    if post is None:
        return None

    post["id"] = str(post.pop("_id"))

    return post


async def save_social_post(post: SocialPost):
    """
    Save a social-media post to MongoDB.

    Uses platform + post_id to prevent
    duplicate social-media posts.
    """

    # ========================================================
    # CHECK FOR EXISTING POST
    # ========================================================

    existing_post = await database.social_posts.find_one(
        {
            "platform": post.source.platform,
            "post_id": post.source.post_id
        }
    )

    if existing_post is not None:

        return {
            "status": "already_exists",
            "post": serialize_social_post(
                existing_post
            )
        }

    # ========================================================
    # CREATE DOCUMENT
    # ========================================================

    now = datetime.now(timezone.utc)

    document = {
        "platform": post.source.platform,
        "post_id": post.source.post_id,

        "author": {
            "username": post.author.username,
            "display_name": post.author.display_name,
            "author_id": post.author.author_id
        },

        "text": post.text,

        "url": (
            str(post.url)
            if post.url
            else None
        ),

        "language": post.language,

        "published_at": post.published_at,

        "engagement": {
            "likes": post.engagement.likes,
            "reposts": post.engagement.reposts,
            "replies": post.engagement.replies,
            "quotes": post.engagement.quotes
        },

        "event_id": post.event_id,

        "created_at": now,
        "updated_at": now
    }

    # ========================================================
    # INSERT
    # ========================================================

    try:

        result = await database.social_posts.insert_one(
            document
        )

    except DuplicateKeyError:

        existing_post = await database.social_posts.find_one(
            {
                "platform": post.source.platform,
                "post_id": post.source.post_id
            }
        )

        return {
            "status": "already_exists",
            "post": serialize_social_post(
                existing_post
            )
        }

    # ========================================================
    # GET SAVED POST
    # ========================================================

    saved_post = await database.social_posts.find_one(
        {
            "_id": result.inserted_id
        }
    )

    return {
        "status": "created",
        "post": serialize_social_post(
            saved_post
        )
    }