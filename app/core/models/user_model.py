from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime

from app.core.models.base_model import BaseModel


class UserModel(BaseModel):
    """Model for table vendors_responses."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    dt_created = Column(DateTime, default=datetime.utcnow)
    dt_updated: Optional[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )  # TODO checar se ta correto on update

    def __repr__(self):
        return f"<UserModel(id={self.id}, name={self.name}, email={self.email})>"
