"""Test PostgreSQL database connection."""

import asyncio
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings


async def test_asyncpg_connection():
    """Test connection using asyncpg directly."""
    print("=" * 60)
    print("Testing asyncpg Connection")
    print("=" * 60)

    # Parse connection URL
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")

    try:
        conn = await asyncpg.connect(db_url)

        # Test query
        version = await conn.fetchval("SELECT version()")
        db_name = await conn.fetchval("SELECT current_database()")
        db_user = await conn.fetchval("SELECT current_user")

        print("[OK] Connected to PostgreSQL")
        print(f"[OK] Database: {db_name}")
        print(f"[OK] User: {db_user}")
        print(f"[OK] Version: {version[:50]}...")

        # Check for tables
        tables = await conn.fetch("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
        """)

        print("\nTables in database:")
        if tables:
            for table in tables:
                print(f"  - {table['tablename']}")
        else:
            print(" (no tables yet - will be created on app startup)")

        await conn.close()
        print("\n[OK] Connection test passed")
        return True

    except asyncpg.InvalidCatalogNameError:
        print("[ERROR] Database 'crud_db' does not exist")
        print("\nCreate it with:")
        print("  psql -U postgres -c 'CREATE DATABASE crud_db;'")
        return False

    except asyncpg.InvalidPasswordError:
        print("[ERROR] Authentication failed")
        print("Check username/password in .env")
        return False

    except Exception as e:
        print(f"[ERROR] Connection failed: {type(e).__name__}")
        print(f"Details: {str(e)}")
        return False


async def test_sqlalchemy_engine():
    """Test connection using SQLAlchemy engine."""
    print("\n" + "=" * 60)
    print("Testing SQLAlchemy Engine")
    print("=" * 60)

    try:
        engine = create_async_engine(settings.database_url, echo=False)

        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            test_val = result.scalar()

        print("[OK] SQLAlchemy engine works")
        print(f"[OK] Test query result: {test_val}")

        await engine.dispose()
        return True

    except Exception as e:
        print(f"[ERROR] SQLAlchemy test failed: {str(e)}")
        return False


async def main():
    """Run all connection tests."""
    print("\nDatabase Connection Test")
    print(f"Connection URL: {settings.database_url[:40]}...")
    print()

    # Test asyncpg
    result1 = await test_asyncpg_connection()

    # Test SQLAlchemy
    result2 = await test_sqlalchemy_engine()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"asyncpg connection: {'PASS' if result1 else 'FAIL'}")
    print(f"SQLAlchemy engine: {'PASS' if result2 else 'FAIL'}")

    if result1 and result2:
        print("\n[SUCCESS] Database ready for application")
        return 0
    else:
        print("\n[FAILED] Fix connection issues before starting app")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
