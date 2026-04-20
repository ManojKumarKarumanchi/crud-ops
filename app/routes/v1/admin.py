"""
Admin Dashboard Routes

Admin-only endpoints for managing users and items.
Requires admin authentication (is_admin=True).
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db import get_db
from app.db.models import User, Item
from app.schemas.user import UserResponse
from app.schemas.item import ItemResponse
from app.auth.security import get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"],
    dependencies=[Depends(get_current_admin_user)]  # All routes require admin
)

logger = logging.getLogger(__name__)


@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    List all users in the system (Admin only).

    **Admin Dashboard Feature:**
    - View all registered users
    - Pagination support
    - Includes admin status and active status

    **Requirements:**
    - Must be authenticated as admin
    - Admin credentials: admin / adminpass123
    """
    logger.info(f"Admin {admin_user.email} requested user list")

    # Get all users with pagination
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()

    logger.info(f"Retrieved {len(users)} users for admin dashboard")
    return list(users)


@router.get("/users/count")
async def get_user_count(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Get total user count (Admin only).

    **Dashboard Metric**
    """
    result = await db.execute(select(func.count(User.id)))
    total = result.scalar()

    # Count active users
    result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active = result.scalar()

    # Count admin users
    result = await db.execute(
        select(func.count(User.id)).where(User.is_admin == True)
    )
    admins = result.scalar()

    logger.info(f"Admin {admin_user.email} requested user statistics")

    return {
        "total_users": total,
        "active_users": active,
        "admin_users": admins,
        "inactive_users": total - active
    }


@router.get("/items", response_model=List[ItemResponse])
async def list_all_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    category: str = Query(None, description="Filter by category"),
    available_only: bool = Query(False, description="Show only available items"),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    List all items in the system (Admin only).

    **Admin Dashboard Feature:**
    - View all products/items
    - Filter by category
    - Filter by availability
    - Pagination support

    **Requirements:**
    - Must be authenticated as admin
    """
    logger.info(f"Admin {admin_user.email} requested item list")

    # Build query
    query = select(Item).order_by(Item.created_at.desc())

    # Apply filters
    if category:
        query = query.where(Item.category == category)
    if available_only:
        query = query.where(Item.is_available == True)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    logger.info(f"Retrieved {len(items)} items for admin dashboard")
    return list(items)


@router.get("/items/count")
async def get_item_count(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Get total item count and statistics (Admin only).

    **Dashboard Metrics**
    """
    # Total items
    result = await db.execute(select(func.count(Item.id)))
    total = result.scalar()

    # Available items
    result = await db.execute(
        select(func.count(Item.id)).where(Item.is_available == True)
    )
    available = result.scalar()

    # Categories
    result = await db.execute(
        select(Item.category, func.count(Item.id))
        .group_by(Item.category)
    )
    categories = dict(result.all())

    logger.info(f"Admin {admin_user.email} requested item statistics")

    return {
        "total_items": total,
        "available_items": available,
        "unavailable_items": total - available,
        "items_by_category": categories
    }


@router.get("/dashboard")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Get complete dashboard summary (Admin only).

    **Overview:**
    - User statistics
    - Item statistics
    - Recent activity
    """
    logger.info(f"Admin {admin_user.email} requested dashboard summary")

    # User stats
    user_count = await db.execute(select(func.count(User.id)))
    active_users = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )

    # Item stats
    item_count = await db.execute(select(func.count(Item.id)))
    available_items = await db.execute(
        select(func.count(Item.id)).where(Item.is_available == True)
    )

    # Recent users (last 5)
    recent_users_result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .limit(5)
    )
    recent_users = recent_users_result.scalars().all()

    # Recent items (last 5)
    recent_items_result = await db.execute(
        select(Item)
        .order_by(Item.created_at.desc())
        .limit(5)
    )
    recent_items = recent_items_result.scalars().all()

    return {
        "statistics": {
            "users": {
                "total": user_count.scalar(),
                "active": active_users.scalar()
            },
            "items": {
                "total": item_count.scalar(),
                "available": available_items.scalar()
            }
        },
        "recent_users": [
            {
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at,
                "is_admin": user.is_admin
            }
            for user in recent_users
        ],
        "recent_items": [
            {
                "title": item.title,
                "price": item.price,
                "category": item.category,
                "created_at": item.created_at
            }
            for item in recent_items
        ]
    }
