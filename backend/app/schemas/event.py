from typing import Optional, Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator


# ============================================================
# EVENT TYPES
# ============================================================

EventType = Literal[
    "natural_disaster",
    "politics",
    "public_health",
    "accident",
    "conflict",
    "economy",
    "technology",
    "other"
]


# ============================================================
# SEVERITY LEVELS
# ============================================================

SeverityLevel = Literal[
    "low",
    "medium",
    "high",
    "critical"
]


# ============================================================
# CREATE EVENT SCHEMA
# ============================================================

class EventCreate(BaseModel):
    """
    Schema used when creating a new event.
    """

    title: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Title of the real-world event"
    )

    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Detailed description of the event"
    )

    event_type: EventType = Field(
        ...,
        description="Category of the event"
    )

    location: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Location associated with the event"
    )

    language: str = Field(
        default="en",
        min_length=2,
        max_length=10,
        description="Language of the event"
    )

    source: str = Field(
        default="manual",
        min_length=2,
        max_length=100,
        description="Source of the event"
    )

    source_url: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Original source URL"
    )

    severity: SeverityLevel = Field(
        default="medium",
        description="Severity level of the event"
    )


    # ========================================================
    # TITLE VALIDATION
    # ========================================================

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Title cannot be empty"
            )

        return value


    # ========================================================
    # DESCRIPTION VALIDATION
    # ========================================================

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Description cannot be empty"
            )

        return value


    # ========================================================
    # EVENT TYPE VALIDATION
    # ========================================================

    @field_validator("event_type", mode="before")
    @classmethod
    def validate_event_type(cls, value):

        if not isinstance(value, str):
            raise ValueError(
                "event_type must be a string"
            )

        return value.strip().lower()


    # ========================================================
    # LOCATION VALIDATION
    # ========================================================

    @field_validator("location")
    @classmethod
    def validate_location(cls, value):

        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


    # ========================================================
    # LANGUAGE VALIDATION
    # ========================================================

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str):

        value = value.strip().lower()

        if not value:
            raise ValueError(
                "Language cannot be empty"
            )

        return value


    # ========================================================
    # SOURCE VALIDATION
    # ========================================================

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str):

        value = value.strip().lower()

        if not value:
            raise ValueError(
                "Source cannot be empty"
            )

        return value


    # ========================================================
    # SOURCE URL VALIDATION
    # ========================================================

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value):

        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        if not (
            value.startswith("http://")
            or value.startswith("https://")
        ):
            raise ValueError(
                "source_url must start with http:// or https://"
            )

        return value


    # ========================================================
    # SEVERITY VALIDATION
    # ========================================================

    @field_validator("severity", mode="before")
    @classmethod
    def validate_severity(cls, value):

        if not isinstance(value, str):
            raise ValueError(
                "severity must be a string"
            )

        value = value.strip().lower()

        return value


# ============================================================
# EVENT RESPONSE SCHEMA
# ============================================================

class EventResponse(BaseModel):
    """
    Schema returned to the frontend.
    """

    id: str

    title: str

    description: str

    event_type: EventType

    location: Optional[str] = None

    language: str

    source: str

    source_url: Optional[str] = None

    severity: SeverityLevel

    model_config = ConfigDict(
        from_attributes=True
    )