"""User Service"""
import re
from typing import List

from app.core.models.user_model import UserModel
from app.core.repositories.user_repository import UserRepository
from app.logger import logger


class UserService:
    """Manages business logic and validations for user operations."""

    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def list_all(self) -> List[dict]:
        """Returns a list of all users."""
        user_models = self.user_repository.fetch_all_users()
        return [user_model.to_dict() for user_model in user_models]

    def get_user(self, user_id) -> dict | None:
        """Returns a user by its id if exists."""
        user_model = self.user_repository.get_user_by_id(user_id)

        return user_model.to_dict() if user_model else None

    def create_user(self, name, email) -> dict | None:
        """Creates a new user if name and email are valid and email is unique."""
        if not (self._is_name_valid(name) and self.is_email_valid(email)) \
                or self.user_repository.get_user_by_email(email):
            logger.error(f"Invalid user data: name={name}, email={email}")
            return None

        user_model = self.user_repository.create_user(UserModel(
            name=name,
            email=email,
        ))

        return user_model.to_dict() if user_model else None

    def update_user(self, user_id, name, email) -> dict | None:
        """Updates a user by its id if exists."""
        user_model = self.user_repository.update_user(UserModel(id=user_id, name=name, email=email))
        return user_model.to_dict() if user_model else None

    def delete_user(self, user_id) -> bool:
        """Deletes a user by its id if exists."""
        return self.user_repository.delete_user(user_id)

    @staticmethod
    def _is_name_valid(name):
        """
        Validate a name string.

        A valid name must:
          - Be at least 2 characters long (after stripping whitespace).
          - Contain only alphabetic characters, spaces, hyphens, or apostrophes.
          - Start and end with an alphabetic character.

        Returns True if the name is valid, False otherwise.
        """
        name = name.strip()
        if len(name) < 2:
            return False

        # - The first character should be a letter.
        # - Allowed characters in the middle: letters, spaces, hyphens, apostrophes.
        # - The last character to be a letter.
        pattern = re.compile(r"^[A-Za-z][A-Za-z\s'-]*[A-Za-z]$")

        return pattern.match(name) is not None

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """
        Validate the email address using a regular expression.
        Returns True if the email is valid, False otherwise.
        """
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return email_regex.match(email) is not None
