from fastapi import APIRouter, HTTPException

from app.database.mongodb import database
from app.schemas.social import SocialPost
from app.services.social_post_service import save_social_post
from app.services.event_correlation import (
    correlate_social_post_with_event
)


router = APIRouter(
    prefix="/social",
    tags=["Social Media"]
)


# ============================================================
# CREATE SOCIAL POST
# ============================================================

@router.post("/posts")
async def create_social_post(post: SocialPost):

    try:

        result = await save_social_post(post)

        return result

    except Exception as error:

        print(
            f"Error saving social post: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to save social post"
        )


# ============================================================
# GET ALL SOCIAL POSTS
# ============================================================

@router.get("/posts")
async def get_social_posts():

    try:

        cursor = database.social_posts.find(
            {}
        ).sort(
            "published_at",
            -1
        )

        posts = []

        async for post in cursor:

            # Convert MongoDB ObjectId
            # to JSON-compatible string

            post["id"] = str(
                post.pop("_id")
            )

            posts.append(post)

        return {
            "count": len(posts),
            "posts": posts
        }

    except Exception as error:

        print(
            f"Error retrieving social posts: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve social posts"
        )


# ============================================================
# GET SINGLE SOCIAL POST
# ============================================================

@router.get("/posts/{post_id}")
async def get_social_post(post_id: str):

    try:

        post = await database.social_posts.find_one(
            {
                "post_id": post_id
            }
        )

        if post is None:

            raise HTTPException(
                status_code=404,
                detail="Social post not found"
            )

        # Convert ObjectId to string

        post["id"] = str(
            post.pop("_id")
        )

        return {
            "post": post
        }

    except HTTPException:

        raise

    except Exception as error:

        print(
            f"Error retrieving social post: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve social post"
        )


# ============================================================
# CORRELATE SOCIAL POST WITH EVENT
# ============================================================

@router.post(
    "/posts/{post_id}/correlate"
)
async def correlate_post(
    post_id: str
):

    try:

        result = await correlate_social_post_with_event(
            post_id=post_id,
            platform="x"
        )

        if result["status"] == "post_not_found":

            raise HTTPException(
                status_code=404,
                detail="Social post not found"
            )

        # ----------------------------------------------------
        # Convert MongoDB ObjectIds
        # ----------------------------------------------------

        if result.get("post"):

            result["post"]["id"] = str(
                result["post"].pop("_id")
            )

        if result.get("event"):

            result["event"]["id"] = str(
                result["event"].pop("_id")
            )

        return result

    except HTTPException:

        raise

    except Exception as error:

        print(
            f"Error correlating social post: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to correlate social post"
        )