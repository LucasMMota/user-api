"""Manages business logic and validations."""
from typing import List

from app.core.models.user_model import UserModel
from app.core.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def list_all(self) -> List[dict]:
        user_models = self.user_repository.fetch_all_users()
        return [user_model.to_dict() for user_model in user_models]

    def get_user(self, user_id) -> dict | None:
        user_model = self.user_repository.get_user_by_id(user_id)

        return user_model.to_dict() if user_model else None

    def create_user(self, name, email) -> dict | None:
        if self.user_repository.get_user_by_email(email):
            return None

        user_model = self.user_repository.create_user(UserModel(
            name=name,
            email=email,
        ))

        return user_model.to_dict() if user_model else None

    def update_user(self, user_id, name, email) -> dict | None:
        user_model = self.user_repository.update_user(UserModel(id=user_id, name=name, email=email))
        return user_model.to_dict() if user_model else None

    def delete_user(self, user_id) -> bool:
        return self.user_repository.delete_user(user_id)
