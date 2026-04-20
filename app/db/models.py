"""SQLAlchemy ORM models."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


def utcnow():
    """Return current UTC time as naive datetime (for PostgreSQL TIMESTAMP columns)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


class Item(Base):
    """Item model for CRUD operations demo."""

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    category = Column(String(100), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)
