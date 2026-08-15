import httpx

from app.config.settings import settings


X_API_URL = "https://api.x.com/2/tweets/search/recent"


async def search_x_posts(
    query: str,
    max_results: int = 10
):
    """
    Search recent public X posts.
    """

    if not settings.x_bearer_token:
        raise ValueError(
            "X_BEARER_TOKEN is not configured"
        )

    if max_results < 10 or max_results > 100:
        raise ValueError(
            "max_results must be between 10 and 100"
        )

    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": (
            "id,text,author_id,created_at,"
            "lang,public_metrics"
        ),
        "expansions": "author_id",
        "user.fields": (
            "id,name,username"
        )
    }

    headers = {
        "Authorization": (
            f"Bearer {settings.x_bearer_token}"
        )
    }

    async with httpx.AsyncClient(
        timeout=15.0
    ) as client:

        response = await client.get(
            X_API_URL,
            params=params,
            headers=headers
        )

    if response.status_code == 401:

        raise ValueError(
            "X API authentication failed. "
            "Check your Bearer Token."
        )

    if response.status_code == 403:

        raise ValueError(
            "X API access forbidden. "
            "Check your developer access and permissions."
        )

    if response.status_code == 429:

        raise ValueError(
            "X API rate limit exceeded."
        )

    response.raise_for_status()

    return response.json()