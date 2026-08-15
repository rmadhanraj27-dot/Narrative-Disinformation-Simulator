from fastapi import APIRouter, HTTPException, Query

from app.services.news_api import search_news
from app.schemas.news import NewsApiResponse
from app.services.news_event_service import save_news_article_as_event


router = APIRouter(
    prefix="/news",
    tags=["News"]
)


# ============================================================
# SEARCH NEWS
# ============================================================

@router.get("/search")
async def search_and_process_news(
    query: str = Query(
        ...,
        min_length=2,
        max_length=200,
        description="News search query"
    ),
    language: str = Query(
        default="en",
        min_length=2,
        max_length=10
    ),
    page_size: int = Query(
        default=5,
        ge=1,
        le=20
    )
):
    """
    Search NewsAPI and convert the returned
    articles into events.
    """

    try:

        # ====================================================
        # STEP 1 — SEARCH NEWSAPI
        # ====================================================

        data = await search_news(
            query=query,
            language=language,
            page_size=page_size
        )

        # ====================================================
        # STEP 2 — VALIDATE RESPONSE
        # ====================================================

        news_response = NewsApiResponse(
            status=data["status"],
            total_results=data.get(
                "totalResults",
                0
            ),
            articles=data.get(
                "articles",
                []
            )
        )

        # ====================================================
        # STEP 3 — PROCESS ARTICLES
        # ====================================================

        results = []

        for article in news_response.articles:

            result = await save_news_article_as_event(
                article
            )

            results.append(
                {
                    "title": article.title,
                    "status": result["status"],
                    "event": result["event"]
                }
            )

        # ====================================================
        # STEP 4 — RETURN RESPONSE
        # ====================================================

        return {
            "query": query,
            "total_results": news_response.total_results,
            "articles_processed": len(results),
            "results": results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        print(
            f"News search error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch and process news"
        )