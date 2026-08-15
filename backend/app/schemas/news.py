from typing import Optional

from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ConfigDict
)


# ============================================================
# NEWS SOURCE
# ============================================================

class NewsSource(BaseModel):
    """
    Information about the publisher of a news article.
    """

    name: Optional[str] = None

    id: Optional[str] = None


# ============================================================
# NEWS ARTICLE
# ============================================================

class NewsArticle(BaseModel):
    """
    Represents a news article received from NewsAPI.
    """

    source: NewsSource

    author: Optional[str] = None

    title: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000
    )

    url: HttpUrl

    image_url: Optional[HttpUrl] = Field(
        default=None,
        alias="urlToImage"
    )

    published_at: datetime = Field(
        ...,
        alias="publishedAt"
    )

    content: Optional[str] = Field(
        default=None,
        max_length=10000
    )

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )


# ============================================================
# NEWS API RESPONSE
# ============================================================

class NewsApiResponse(BaseModel):
    """
    Complete response returned by NewsAPI.
    """

    status: str

    total_results: int = Field(
        default=0,
        alias="totalResults"
    )

    articles: list[NewsArticle] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )