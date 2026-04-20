"""Pydantic schemas for Item model."""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    """Schema for creating an item."""

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    price: int = Field(ge=0, description="Price in cents")
    category: Optional[str] = Field(None, max_length=100)
    is_available: bool = True


class ItemUpdate(BaseModel):
    """Schema for updating an item."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    is_available: Optional[bool] = None


class ItemResponse(BaseModel):
    """Schema for item response."""

    id: UUID
    title: str
    description: Optional[str] = None
    price: int
    category: Optional[str] = None
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration for ItemResponse schema."""
        from_attributes = True
