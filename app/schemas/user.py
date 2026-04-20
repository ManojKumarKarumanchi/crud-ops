"""Pydantic schemas for User model."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=72,
        description="Password (8-72 characters, bcrypt limit)"
    )
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""

    id: UUID
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for JWT token payload."""

    email: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str
