# Base Database Model - provides base model class with common fields and methods for all database models
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, Integer, DateTime

from app import db


# Base model class with common fields - all models should inherit from this to get id, timestamps, and utility methods
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Convert model instance to dictionary
    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    # Update model fields with provided values
    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # String representation of the model
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"

