"""Encapsulates direct database operations."""
from typing import List

from app.core.models.user_model import UserModel
from app.core.repositories.base_repository import BaseRepository
from app.core.schemas.user_schema import UserSchema
from app.logger import logger


class UserRepository(BaseRepository):
    """Interface to handle interactions with database via SQLAlchemy model objects."""

    def __init__(self):
        super().__init__(schema=UserSchema)

    def fetch_all_users(self) -> List[UserSchema]:
        """Fetches all users from database (without limit or pagination)."""
        with self.db_session as db_session:
            user_models = db_session.query(UserModel).all()
            return [UserSchema.from_orm(user) for user in user_models]

    def get_user_by_id(self, user_id: int) -> UserSchema | None:
        """Fetches a user by id."""
        with self.db_session as db_session:
            user_models = (
                db_session.query(UserModel).filter(UserModel.id == user_id).first()
            )
            return self.from_orm(user_models)

    def get_user_by_email(self, email: str) -> UserSchema | None:
        """Fetches a user by email."""
        with self.db_session as db_session:
            user_models = (
                db_session.query(UserModel).filter(UserModel.email == email).first()
            )
            return self.from_orm(user_models)

    def create_user(self, user: UserModel) -> UserSchema | None:
        """Creates a user and return the created user object."""
        with self.db_session as db_session:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

            return self.from_orm(user)

    def update_user(self, user) -> UserSchema | None:
        """Updates a user and return the updated user object."""
        with self.db_session as db_session:
            _user = db_session.query(UserModel).filter(UserModel.id == user.id).first()
            if not user:
                logger.error(f"m=update_user, User {user.id} not found")
                return None

            _user.name = user.name
            _user.email = user.email

            db_session.commit()
            db_session.refresh(_user)

            return self.from_orm(_user)

    def delete_user(self, user_id) -> bool:
        """Deletes an user if exists and return True if the user was deleted."""
        with self.db_session as db_session:
            user = db_session.query(UserModel).filter(UserModel.id == user_id).first()
            if user is None:
                logger.error(f"m=delete_user, User {user_id} not found")
                return False

            db_session.delete(user)
            db_session.commit()

            return True
