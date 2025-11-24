from datetime import datetime
from uuid import UUID

from app.dto.balance_change import BalanceChangeResponse, BalanceChangeRequest
from domain.entity.account import Account
from domain.entity.balance_change import BalanceChange, BalanceChangeState
from infra.db.account import AccountRepository
from infra.db.balance_change import BalanceChangeRepository


class BalanceChangeUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
        balance_change_repository: BalanceChangeRepository,
    ):
        self.account_repository = account_repository
        self.balance_change_repository = balance_change_repository

    async def get_change_for_account(
        self, account_id: UUID
    ) -> list[BalanceChangeResponse]:
        changes = await self.balance_change_repository.get_by_account_id(account_id)

        return [BalanceChangeResponse.model_validate(change) for change in changes]

    async def new_balance_update(
        self, request_dto: BalanceChangeRequest
    ) -> BalanceChangeResponse:
        account = await self.account_repository.get_by_name(request_dto.account_name)
        if not account:
            account = Account(
                name=request_dto.account_name,
                current_balance=request_dto.balance,
                last_balance_update=datetime.now(),
            )

            account = await self.account_repository.create(account)

        diff = (
            0
            if request_dto.state
            in [BalanceChangeState.MONEY_RECIEVED, BalanceChangeState.MONEY_WITHDRAW]
            else request_dto.balance - account.current_balance
        )
        balance_change = BalanceChange(
            account_id=account.id,
            state=request_dto.state.value,
            balance=request_dto.balance,
            balance_diff=diff,
        )

        balance_change = await self.balance_change_repository.create(balance_change)
        account.current_balance = request_dto.balance
        await self.account_repository.update(account)

        return BalanceChangeResponse.model_validate(balance_change)
