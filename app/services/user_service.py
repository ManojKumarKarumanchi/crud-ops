"""User service for business logic."""

import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.db.models import User
from app.schemas.user import UserCreate
from app.auth.security import get_password_hash, verify_password

logger = logging.getLogger(__name__)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get user by email."""
    try:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Database error fetching user {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user."""
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, user_data.email)
        if existing_user:
            logger.warning(f"User registration failed: {user_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        logger.info(f"User created: {db_user.email}")
        return db_user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user {user_data.email}: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password."""
    try:
        user = await get_user_by_email(db, email)
        if not user:
            logger.warning(f"Login failed: user {email} not found")
            return None
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Login failed: invalid password for {email}")
            return None

        logger.info(f"User authenticated: {email}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error authenticating user {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication error occurred"
        )
