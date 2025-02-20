"""SQLAlchemy base model. Handles ORM operations for inherited models."""
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()
