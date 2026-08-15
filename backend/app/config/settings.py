from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Narrative Disinformation Simulator"
    app_version: str = "1.0.0"

    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "narrative_disinformation_db"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    news_api_key: str = ""

    x_bearer_token: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()