"""Encapsulates direct database operations."""
from typing import List

from app.core.models.user_model import UserModel
from app.core.repositories.base_repository import BaseRepository
from app.core.schemas.user_schema import UserSchema


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(schema=UserSchema)

    def fetch_all_users(self) -> List[UserSchema]:
        with self.db_session as db_session:
            user_models = (
                db_session.query(UserModel)
                .all()
            )
            return [UserSchema.from_orm(user) for user in user_models]

    def get_user_by_id(self, user_id: int) -> UserSchema:
        with self.db_session as db_session:
            user_models = (
                db_session.query(UserModel)
                .filter(
                    UserModel.id == user_id
                )
                .first()
            )
            return self.from_orm(user_models)

    def get_user_by_email(self, email: str) -> UserSchema:
        with self.db_session as db_session:
            user_models = (
                db_session.query(UserModel)
                .filter(
                    UserModel.email == email
                )
                .first()
            )
            return self.from_orm(user_models)

    def create_user(self, user: UserModel) -> UserSchema:
        """
        Expects a User object without an id.
        Returns the newly created User (with id set).
        """
        with self.db_session as db_session:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

            return self.from_orm(user)

    def update_user(self, user) -> UserSchema | None:
        """
        Expects a User object with a valid id.
        Returns the updated User if successful, or None if user does not exist.
        """
        with self.db_session as db_session:
            _user = db_session.query(UserModel).filter(UserModel.id == user.id).first()
            if not user:
                return None

            _user.name = user.name
            _user.email = user.email

            db_session.commit()
            db_session.refresh(_user)

            return self.from_orm(_user)

    def delete_user(self, user_id) -> bool:
        """
        Deletes a user by ID.
        Returns True if a user was deleted, False otherwise.
        """
        with self.db_session as db_session:
            user = db_session.query(UserModel).filter(UserModel.id == user_id).first()
            if user is None:
                return False

            db_session.delete(user)
            db_session.commit()

            return True
