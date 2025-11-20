from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool

from infra.utils.config import DatabaseConfig
from infra.utils.log import logger


class Database:
    def __init__(self, engine: AsyncEngine):
        self.session_factory = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self):
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.commit()


class DatabaseManager:
    _db_instance: Database | None = None

    @classmethod
    def init_db(cls, config: DatabaseConfig) -> Database:
        if cls._db_instance is not None:
            return cls._db_instance

        if config.use_pgbouncer:
            logger.info("Using PgBouncer connection settings")

            engine = create_async_engine(
                config.dsn,
                echo=False,
                poolclass=NullPool,
                pool_pre_ping=True,  # Add health check capability
                connect_args={
                    # Disable prepared statements (required for PgBouncer)
                    "statement_cache_size": 0,
                    # Connection and command timeouts
                    "timeout": 10,  # Connection timeout in seconds
                    "command_timeout": 30,  # Timeout for operations in seconds
                },
            )
        else:
            engine = create_async_engine(
                config.dsn,
                echo=False,
                pool_size=10,  # Start with fewer connections
                max_overflow=20,  # Allow more connections during spikes
                pool_timeout=30,  # Wait time for a connection from pool
                pool_recycle=1800,  # Recycle connections after 30 minutes
                pool_pre_ping=True,  # Verify connections before using them
            )

        cls._db_instance = Database(engine)

        return cls._db_instance

    @classmethod
    def init_test_db(cls, db: Database) -> Database:
        cls._db_instance = db

        return cls._db_instance

    @classmethod
    def get_db_instance(cls) -> Database | None:
        return cls._db_instance
