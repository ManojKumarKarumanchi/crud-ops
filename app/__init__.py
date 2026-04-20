"""FastAPI application initialization."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logger import setup_logging
from app.db import init_db
from app.routes import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    import os
    # Startup
    setup_logging()
    await init_db()

    # Optional: seed database on first deploy (only if empty)
    if os.getenv("SEED_DATABASE", "false").lower() == "true":
        from seed_database import seed_admin, seed_users, seed_items
        from app.db import SessionLocal
        from app.db.models import User
        from sqlalchemy import select

        async with SessionLocal() as db:
            try:
                # Check if DB already has data
                result = await db.execute(select(User).limit(1))
                if result.scalar_one_or_none():
                    print("[INFO] Database already seeded, skipping")
                else:
                    await seed_admin(db)
                    await seed_users(db, 6)
                    await seed_items(db, 6)
                    print("[INFO] Database seeded successfully")
            except Exception as e:
                print(f"[ERROR] Seeding failed: {e}")
                await db.rollback()

    yield
    # Shutdown (cleanup if needed)


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI CRUD API with JWT Authentication. **Note:** Use email address as username for login.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(v1_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "CRUD API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
