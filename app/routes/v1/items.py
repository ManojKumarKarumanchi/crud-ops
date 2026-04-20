"""Item CRUD routes."""

import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.db.models import User
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import (
    get_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item
)
from app.auth.security import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all items (protected route)."""
    logger.info(f"Items list requested by {current_user.email}")
    items = await get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific item by ID (protected route)."""
    logger.info(f"Item {item_id} requested by {current_user.email}")
    item = await get_item_by_id(db, item_id)
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_new_item(
    item_data: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new item (protected route)."""
    logger.info(f"Item creation requested by {current_user.email}")
    item = await create_item(db, item_data)
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_existing_item(
    item_id: UUID,
    item_data: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing item (protected route)."""
    logger.info(f"Item {item_id} update requested by {current_user.email}")
    item = await update_item(db, item_id, item_data)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an item (protected route)."""
    logger.info(f"Item {item_id} deletion requested by {current_user.email}")
    await delete_item(db, item_id)
    return None
