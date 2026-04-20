"""Authentication routes."""

import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import create_user, authenticate_user
from app.auth.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    Create a new account with email and password.
    After registration, use the login endpoint to get an access token.
    """
    logger.info(f"Registration attempt: {user_data.email}")
    user = await create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login and get JWT access token.

    **Note:** Use your email address as the username.

    - **username**: Your email address (e.g., user@example.com)
    - **password**: Your password
    """
    logger.info(f"Login attempt: {form_data.username}")
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    logger.info(f"Login successful: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}
