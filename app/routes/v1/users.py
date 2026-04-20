"""User routes."""

import logging
from fastapi import APIRouter, Depends

from app.db.models import User
from app.schemas.user import UserResponse
from app.auth.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    logger.info(f"User info requested: {current_user.email}")
    return current_user
