import logging
from logging.config import dictConfig
from pydantic import BaseModel

from app.settings import settings


class LogConfig(BaseModel):
    """Logging configuration for the application."""
    LOG_LEVEL: str = settings.LOG_LEVEL
    LOGGER_NAME: str = settings.PROJECT_NAME
    LOG_FORMAT: str = "%(levelname)s | %(asctime)s | %(message)s"

    # Standard logging config keys
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "format": "%(levelname)s | %(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    }
    handlers: dict = {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        }
    }

    def dict(self, **kwargs):
        """Override to inject dynamic logger configuration."""
        config = super().dict(**kwargs)
        config["loggers"] = {
            self.LOGGER_NAME: {"handlers": ["default"], "level": self.LOG_LEVEL}
        }
        return config


# Configure logging using the dictionary configuration
logger_config = LogConfig()
dictConfig(logger_config.dict())
logger = logging.getLogger(logger_config.LOGGER_NAME)
