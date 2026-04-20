"""Item service for business logic."""

import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.db.models import Item
from app.schemas.item import ItemCreate, ItemUpdate

logger = logging.getLogger(__name__)


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get all items with pagination."""
    try:
        result = await db.execute(select(Item).offset(skip).limit(limit))
        items = result.scalars().all()
        logger.info(f"Retrieved {len(items)} items")
        return list(items)
    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch items"
        )


async def get_item_by_id(db: AsyncSession, item_id: UUID) -> Optional[Item]:
    """Get item by ID."""
    try:
        result = await db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch item"
        )


async def create_item(db: AsyncSession, item_data: ItemCreate) -> Item:
    """Create a new item."""
    try:
        db_item = Item(**item_data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)

        logger.info(f"Item created: {db_item.title} (ID: {db_item.id})")
        return db_item

    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )


async def update_item(db: AsyncSession, item_id: UUID, item_data: ItemUpdate) -> Item:
    """Update an existing item."""
    try:
        db_item = await get_item_by_id(db, item_id)
        if not db_item:
            logger.warning(f"Update failed: item {item_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        # Update only provided fields
        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)

        await db.commit()
        await db.refresh(db_item)

        logger.info(f"Item updated: {db_item.title} (ID: {db_item.id})")
        return db_item

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update item"
        )


async def delete_item(db: AsyncSession, item_id: UUID) -> bool:
    """Delete an item."""
    try:
        db_item = await get_item_by_id(db, item_id)
        if not db_item:
            logger.warning(f"Delete failed: item {item_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        await db.delete(db_item)
        await db.commit()

        logger.info(f"Item deleted: ID {item_id}")
        return True

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )
