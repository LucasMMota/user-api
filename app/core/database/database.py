"""Database connection and session handling."""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.models.base_model import BaseModel
from app.settings import settings


class Database:
    """Handles database connection."""

    DATABASE_URL = (
        "sqlite:///{db_path}"
    )

    @staticmethod
    def engine() -> Engine:
        """Creates a database engine."""
        return create_engine(
            Database.DATABASE_URL.format(
                db_path=settings.DB_PATH
            )
        )

    @classmethod
    def recreate_db(cls):
        """Drops all tables and then recreates them."""
        engine = cls.engine()
        BaseModel.metadata.drop_all(bind=engine)
        BaseModel.metadata.create_all(bind=engine)

    @classmethod
    def initialize_db(cls):
        """Initializes database and creates tables, based on models that inherits from BaseModel."""
        BaseModel.metadata.create_all(bind=Database.engine())

    @staticmethod
    def __get_session() -> Session:
        """Creates a local session and returns it."""
        session_class = sessionmaker(
            autocommit=False, autoflush=False, bind=Database.engine()
        )
        return session_class()

    @staticmethod
    @contextmanager
    def create_new_session() -> Generator[Session, None, None]:
        """Initializes a new db session and returns it."""
        db = Database.__get_session()
        try:
            yield db
        finally:
            db.close()
