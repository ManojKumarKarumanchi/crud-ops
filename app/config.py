"""Application configuration using Pydantic Settings.

All configuration is loaded from environment variables (.env file).
Pydantic Settings automatically handles os.getenv() internally.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables are loaded from .env file automatically.
    No hardcoded values - all must be set in .env or have safe defaults.
    """

    # Database - REQUIRED in .env
    database_url: str = Field(
        ...,  # Required field, no default
        description="PostgreSQL database URL with asyncpg driver"
    )

    @field_validator('database_url')
    @classmethod
    def transform_database_url(cls, v: str) -> str:
        """Transform DATABASE_URL to use asyncpg driver if needed."""
        if v.startswith('postgresql://'):
            # Railway provides postgresql://, but we need postgresql+asyncpg://
            return v.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return v

    # JWT Authentication - REQUIRED in .env
    secret_key: str = Field(
        ...,  # Required field, no default - must generate secure key
        description="Secret key for JWT token signing (generate with secrets.token_hex(32))"
    )

    # JWT Configuration - Safe defaults, can override in .env
    algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="JWT token expiration time in minutes"
    )

    # Application Settings - Safe defaults, can override in .env
    app_name: str = Field(
        default="CRUD API",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode (NEVER True in production)"
    )
    seed_database: bool = Field(
        default=False,
        description="Seed database with test data on startup (only if DB empty)"
    )

    class Config:
        """Pydantic Settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Optional: Set to True to require .env file
        # env_file_required = True


# Load settings from environment
# Pydantic automatically reads from .env and os.environ
settings = Settings()
