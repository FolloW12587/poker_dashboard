from datetime import datetime
from uuid import UUID
from fastapi import APIRouter

from app.dto.balance_change import BalanceChangeResponse, NewBalanceChangeRequest
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
    date_from: datetime | None,
    date_to: datetime | None,
    _: CurrentUserDep,
) -> list[BalanceChangeResponse]:
    return await use_case.get_change_for_account(account_id, date_from, date_to)


@router.post("/")
async def new_balance_change(
    use_case: BalanceChangeUseCaseDep,
    request_dto: NewBalanceChangeRequest,
    _: VerifiedApiCallDep,
) -> BalanceChangeResponse:
    return await use_case.new_balance_update(request_dto)
