# --- Configuration ---


from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from app.dto.auth import TokenUser
from app.usecase.account import AccountUseCase
from app.usecase.auth import AuthUseCase
from app.usecase.balance_change import BalanceChangeUseCase

from infra.db.conn import DatabaseManager
from infra.db.account import AccountRepository
from infra.db.balance_change import BalanceChangeRepository
from infra.db.user import UserRepository
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


def get_account_repository(db_session: DbSessionDep) -> AccountRepository:
    return AccountRepository(db_session)


AccountRepDep = Annotated[AccountRepository, Depends(get_account_repository)]


def get_balance_change_repository(db_session: DbSessionDep) -> BalanceChangeRepository:
    return BalanceChangeRepository(db_session)


BalanceChangeRepDep = Annotated[
    BalanceChangeRepository, Depends(get_balance_change_repository)
]


def get_user_repository(db_session: DbSessionDep) -> UserRepository:
    return UserRepository(db_session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

# --- UseCase ---


def get_account_usecase(account_repo: AccountRepDep):
    return AccountUseCase(account_repo)


AccountUseCaseDep = Annotated[AccountUseCase, Depends(get_account_usecase)]


def get_auth_usecase(cfg: ConfigDep, user_repo: UserRepositoryDep):
    return AuthUseCase(cfg.auth, user_repo)


AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_usecase)]


def get_balance_change_usecase(
    account_repo: AccountRepDep, balance_change_repo: BalanceChangeRepDep
):
    return BalanceChangeUseCase(account_repo, balance_change_repo)


BalanceChangeUseCaseDep = Annotated[
    BalanceChangeUseCase, Depends(get_balance_change_usecase)
]


# --- Auth ---

security = HTTPBearer()


async def get_current_user(
    auth_use_case: AuthUseCaseDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> TokenUser:
    return auth_use_case.get_user_from_token(credentials.credentials)


CurrentUserDep = Annotated[TokenUser, Depends(get_current_user)]


async def get_request_api_key(
    request: Request,
) -> str:
    api_key = request.query_params.get("api_key")
    if api_key:
        return api_key

    try:
        body = await request.json()
        if isinstance(body, dict) and "api_key" in body:
            return body["api_key"]
    except Exception:
        # тело не JSON — игнорируем
        pass

    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")


async def verify_api_call(
    auth_use_case: AuthUseCaseDep,
    api_key: Annotated[str, Depends(get_request_api_key)],
) -> bool:
    return auth_use_case.validate_api_secret(api_key)


VerifiedApiCallDep = Annotated[bool, Depends(verify_api_call)]
