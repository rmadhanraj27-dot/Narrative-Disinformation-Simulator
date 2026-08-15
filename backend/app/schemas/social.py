from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, ConfigDict


# ============================================================
# SOCIAL MEDIA SOURCE
# ============================================================

class SocialMediaSource(BaseModel):
    """
    Identifies the social media platform.
    """

    platform: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    post_id: str = Field(
        ...,
        min_length=1,
        max_length=200
    )


# ============================================================
# SOCIAL MEDIA AUTHOR
# ============================================================

class SocialMediaAuthor(BaseModel):
    """
    Basic information about the author of a social-media post.
    """

    username: Optional[str] = Field(
        default=None,
        max_length=100
    )

    display_name: Optional[str] = Field(
        default=None,
        max_length=200
    )

    author_id: Optional[str] = Field(
        default=None,
        max_length=200
    )


# ============================================================
# SOCIAL MEDIA ENGAGEMENT
# ============================================================

class SocialMediaEngagement(BaseModel):
    """
    Engagement information associated with a social-media post.
    """

    likes: int = Field(
        default=0,
        ge=0
    )

    reposts: int = Field(
        default=0,
        ge=0
    )

    replies: int = Field(
        default=0,
        ge=0
    )

    quotes: int = Field(
        default=0,
        ge=0
    )


# ============================================================
# SOCIAL MEDIA POST
# ============================================================

class SocialPost(BaseModel):
    """
    Represents a social-media post collected by the system.
    """

    source: SocialMediaSource

    author: SocialMediaAuthor

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )

    url: Optional[HttpUrl] = None

    language: str = Field(
        default="en",
        min_length=2,
        max_length=10
    )

    published_at: datetime

    engagement: SocialMediaEngagement = Field(
        default_factory=SocialMediaEngagement
    )

    event_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )


# ============================================================
# SOCIAL POST RESPONSE
# ============================================================

class SocialPostResponse(BaseModel):
    """
    Response representation of a stored social-media post.
    """

    id: str

    platform: str

    post_id: str

    username: Optional[str] = None

    text: str

    url: Optional[HttpUrl] = None

    language: str

    published_at: datetime

    engagement: SocialMediaEngagement

    event_id: Optional[str] = None

    created_at: datetime

    updated_at: datetime