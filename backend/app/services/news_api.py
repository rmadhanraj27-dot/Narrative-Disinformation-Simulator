import httpx

from app.config.settings import settings


NEWS_API_URL = "https://newsapi.org/v2/everything"


async def search_news(
    query: str,
    language: str = "en",
    page_size: int = 10
):
    """
    Search NewsAPI for articles matching a query.
    """

    if not settings.news_api_key:
        raise ValueError(
            "NEWS_API_KEY is not configured"
        )

    params = {
        "q": query,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": page_size
    }

    headers = {
        "X-Api-Key": settings.news_api_key
    }

    async with httpx.AsyncClient(
        timeout=15.0
    ) as client:

        response = await client.get(
            NEWS_API_URL,
            params=params,
            headers=headers
        )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise ValueError(
            data.get(
                "message",
                "News API request failed"
            )
        )

    return data