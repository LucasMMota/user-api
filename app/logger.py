import logging
from logging.config import dictConfig

from pydantic import BaseModel

from app.core.settings import settings


class LogConfig(BaseModel):
    """Logging configuration to be set for the server."""

    # Priority order: ERROR, WARNING, INFO, DEBUG
    LOG_LEVEL: str = settings.LOG_LEVEL

    LOGGER_NAME: str = settings.PROJECT_NAME
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"

    # Logging config
    version = 1
    disable_existing_loggers = False
    # formatters = {
    #     "default": {
    #         "()": "uvicorn.logging.DefaultFormatter",
    #         "fmt": LOG_FORMAT,
    #         "datefmt": "%Y-%m-%d %H:%M:%S",
    #     },
    # }
    # handlers = {
    #     "default": {
    #         "formatter": "default",
    #         "class": "logging.StreamHandler",
    #         "stream": "ext://sys.stderr",
    #     },
    # }

    def dict(self, **kwargs):
        """Overwrites the super method, so we can reset log level."""
        return {**super().dict(**kwargs), **self.loggers}

    @property
    def loggers(self):
        """Implements loggers property to be dynamically changeable."""
        return {
            "loggers": {
                self.LOGGER_NAME: {"handlers": ["default"], "level": self.LOG_LEVEL},
            }
        }


logger_config = LogConfig()
dictConfig(logger_config.dict())
logger = logging.getLogger(logger_config.LOGGER_NAME)
