"""Base repository class for all repository classes."""
from typing import Generator

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database.database import Database
from app.core.models.user_model import UserModel


class BaseRepository:
    """Base interface for repository classes."""

    def __init__(self, schema):
        self.schema = schema

    @property
    def db_session(self) -> Generator[Session, None, None]:
        """Creates a new db session."""
        return Database.create_new_session()

    def from_orm(self, user_model: UserModel) -> None | BaseModel:
        """Converts an SQLAlchemy UserModel got from databse into a Pydantic BaseModel object."""
        if not user_model:
            return None

        return self.schema.from_orm(user_model)
