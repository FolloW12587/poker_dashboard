from fastapi import APIRouter

from app.dto.account import AccountResponse
from presentation.rest.deps import AccountUseCaseDep, CurrentUserDep

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
async def get_accounts(
    use_case: AccountUseCaseDep,
    _: CurrentUserDep,
) -> list[AccountResponse]:
    return await use_case.get_accounts()
