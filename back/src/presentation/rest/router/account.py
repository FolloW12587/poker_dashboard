from fastapi import APIRouter

from app.dto.account import AccountResponse
from presentation.rest.deps import AccountUseCase

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/")
async def get_accounts(
    use_case: AccountUseCase,
) -> list[AccountResponse]:
    return await use_case.get_accounts()
