import re
from typing import Optional

from app.schemas.news import NewsArticle
from app.schemas.event import EventCreate


# ============================================================
# EVENT TYPE KEYWORDS
# ============================================================

EVENT_TYPE_KEYWORDS = {
    "natural_disaster": [
        "earthquake",
        "flood",
        "flooding",
        "cyclone",
        "hurricane",
        "tsunami",
        "landslide",
        "drought",
        "wildfire",
        "forest fire",
        "volcanic",
        "volcano",
        "storm",
        "heavy rainfall",
        "heavy rain"
    ],

    "politics": [
        "election",
        "government",
        "minister",
        "president",
        "prime minister",
        "parliament",
        "political",
        "vote",
        "poll"
    ],

    "public_health": [
        "disease",
        "outbreak",
        "epidemic",
        "pandemic",
        "virus",
        "infection",
        "health emergency",
        "hospital"
    ],

    "accident": [
        "accident",
        "crash",
        "collision",
        "explosion",
        "fire",
        "derailment",
        "road accident"
    ],

    "conflict": [
        "war",
        "attack",
        "military",
        "conflict",
        "clash",
        "missile",
        "bombing",
        "strike"
    ],

    "economy": [
        "inflation",
        "recession",
        "stock market",
        "market crash",
        "interest rate",
        "unemployment",
        "economy",
        "economic crisis"
    ],

    "technology": [
        "cyberattack",
        "cyber attack",
        "data breach",
        "artificial intelligence",
        "ai",
        "technology",
        "software",
        "hacking",
        "hack",
        "server outage",
        "internet outage"
    ]
}


# ============================================================
# SEVERITY KEYWORDS
# ============================================================

SEVERITY_KEYWORDS = {
    "critical": [
        "catastrophic",
        "massive casualties",
        "state of emergency",
        "major disaster",
        "deadly",
        "fatal",
        "severe crisis"
    ],

    "high": [
        "severe",
        "major",
        "dangerous",
        "significant",
        "large-scale",
        "heavy",
        "serious"
    ],

    "medium": [
        "moderate",
        "concern",
        "warning",
        "increased",
        "rising"
    ]
}


# ============================================================
# LOCATION EXTRACTION
# ============================================================

def extract_location(
    text: str
) -> Optional[str]:
    """
    Performs a simple location extraction using
    common location patterns.

    This is intentionally rule-based for Phase 3.9.3.
    A proper NER model will replace this later.
    """

    patterns = [
        r"\bin\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})",
        r"\bat\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})",
        r"\bnear\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            location = match.group(1).strip()

            return location

    return None


# ============================================================
# EVENT TYPE DETECTION
# ============================================================

def detect_event_type(
    text: str
) -> str:

    text = text.lower()

    scores = {}

    for event_type, keywords in EVENT_TYPE_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:

                score += 1

        if score > 0:

            scores[event_type] = score

    if not scores:

        return "other"

    return max(
        scores,
        key=scores.get
    )


# ============================================================
# SEVERITY DETECTION
# ============================================================

def detect_severity(
    text: str
) -> str:

    text = text.lower()

    for severity, keywords in SEVERITY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                return severity

    return "medium"


# ============================================================
# NEWS → EVENT
# ============================================================

def news_article_to_event(
    article: NewsArticle
) -> EventCreate:
    """
    Converts a NewsArticle into an EventCreate object.
    """

    description = (
        article.description
        or article.content
        or article.title
    )

    combined_text = " ".join(
        [
            article.title,
            description
        ]
    )

    event_type = detect_event_type(
        combined_text
    )

    severity = detect_severity(
        combined_text
    )

    location = extract_location(
        combined_text
    )

    source_name = (
        article.source.name
        or "newsapi"
    )

    event = EventCreate(

        title=article.title,

        description=description,

        event_type=event_type,

        location=location,

        language="en",

        source=source_name,

        source_url=str(article.url),

        severity=severity
    )

    return event