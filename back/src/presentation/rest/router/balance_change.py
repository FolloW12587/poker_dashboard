from uuid import UUID
from fastapi import APIRouter

from app.dto.balance_change import BalanceChangeResponse, BalanceChangeRequest
from presentation.rest.deps import (
    BalanceChangeUseCaseDep,
    CurrentUserDep,
    VerifiedApiCallDep,
)

router = APIRouter(prefix="/balance_change", tags=["balance_change"])


@router.get("/{account_id}")
async def get_account_balance_change(
    use_case: BalanceChangeUseCaseDep,
    account_id: UUID,
    _: CurrentUserDep,
) -> list[BalanceChangeResponse]:
    return await use_case.get_change_for_account(account_id)


@router.post("/")
async def new_balance_change(
    use_case: BalanceChangeUseCaseDep,
    request_dto: BalanceChangeRequest,
    _: VerifiedApiCallDep,
) -> BalanceChangeResponse:
    return await use_case.new_balance_update(request_dto)
