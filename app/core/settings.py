from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings configuration mapping."""

    PROJECT_NAME: str = "picpay-api"
    LOG_LEVEL = "INFO"

    API_V1_PREFIX: str = "/v1"

    # TODO mover pro arquivo de venv
    DB_PATH: str = "pic_pay_api_db.db"


settings = Settings()
