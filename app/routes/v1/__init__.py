"""V1 API routes aggregation."""

from fastapi import APIRouter
from app.routes.v1 import auth, users, items, admin

router = APIRouter(prefix="/v1")

# Include all v1 routers
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(items.router)
router.include_router(admin.router)
