import pytest_asyncio
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# from presentation.rest.app import app

# from infra.db import models  # pylint: disable=unused-import
from domain.entity.base import BaseEntity

# from infra.db.conn import Database, DatabaseManager

# Create a test database URL
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

# Create a test database engine and session factory
test_engine = create_async_engine(TEST_DB_URL, echo=True, poolclass=StaticPool)
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="module")
async def test_db():
    # Initialize the test database
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)

    yield

    # Drop the test database
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(test_db):
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
