# --- Configuration ---


from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.usecase.account import AccountUseCase

from infra.db.conn import DatabaseManager
from infra.db.account import AccountRepository
from infra.utils.config import Config, load_config

# --- Configuration ---

ConfigDep = Annotated[Config, Depends(load_config)]


# --- Database ---


async def get_db(config: ConfigDep) -> AsyncGenerator[AsyncSession, None]:
    db = DatabaseManager.get_db_instance()

    if db is None:
        db = DatabaseManager.init_db(config.db)

    async with db.session() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_user_repository(db_session: DbSessionDep) -> AccountRepository:
    return AccountRepository(db_session)


UserRepDep = Annotated[AccountRepository, Depends(get_user_repository)]
