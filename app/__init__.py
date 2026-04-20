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
    # Startup
    setup_logging()
    await init_db()
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
