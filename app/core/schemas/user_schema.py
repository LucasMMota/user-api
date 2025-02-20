from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Schema for table vendors_responses."""

    id: int
    name: str
    email: str
    dt_created: datetime
    dt_updated: datetime

    class Config:
        """Pydantic's config."""

        orm_mode = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dt_created": self.dt_created,
            "dt_updated": self.dt_updated,
        }
