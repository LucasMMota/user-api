from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings configuration mapping."""

    PROJECT_NAME: str = "user-api"
    LOG_LEVEL = "INFO"

    API_PREFIX: str = "/api"
    API_V1_PREFIX: str = "/v1"

    DB_PATH: str = "user_api_db.db"


settings = Settings()
