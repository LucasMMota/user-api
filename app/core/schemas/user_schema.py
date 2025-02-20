"""User schema."""
from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Schema for table users."""

    id: int
    name: str
    email: str
    dt_created: datetime
    dt_updated: datetime

    class Config:
        """
        Pydantic's config.

        This allows to bind an instance of ORM objects—like SQLAlchemy to instances of a Pydantic model.
        UserSchema.from_orm(user_model) will convert a SQLAlchemy UserModel object to a Pydantic (BaseModel) object.
        """

        orm_mode = True

    def to_dict(self):
        """Converts the Pydantic model to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dt_created": self.dt_created,
            "dt_updated": self.dt_updated,
        }
