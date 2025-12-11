from asyncio import sleep
from datetime import datetime
from uuid import UUID

from app.dto.balance_change import BalanceChangeResponse, NewBalanceChangeRequest
from app.usecase.errors import InvalidInputError
from domain.entity.account import Account
from domain.entity.balance_change import BalanceChange, BalanceChangeState
from infra.db.account import AccountRepository
from infra.db.balance_change import BalanceChangeRepository


from infra.utils.log import logger


class BalanceChangeUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
        balance_change_repository: BalanceChangeRepository,
    ):
        self.account_repository = account_repository
        self.balance_change_repository = balance_change_repository

    async def get_change_for_account(
        self, account_id: UUID, date_from: datetime | None, date_to: datetime | None
    ) -> list[BalanceChangeResponse]:
        changes = await self.balance_change_repository.get_by_account_id(
            account_id, date_from, date_to
        )
        await sleep(5)

        return [BalanceChangeResponse.model_validate(change) for change in changes]

    async def new_balance_update(
        self, request_dto: NewBalanceChangeRequest
    ) -> BalanceChangeResponse:
        logger.info("New balance change for account %s", request_dto.account_name)

        if request_dto.state in [
            BalanceChangeState.DEPOSIT,
            BalanceChangeState.WITHDRAW,
        ]:
            raise InvalidInputError(
                "You can't send balance change with DEPOSIT and WITHDRAW states"
            )

        account = await self.account_repository.get_by_name(request_dto.account_name)
        if not account:
            logger.info("No account found. Creating...")
            account = Account(
                name=request_dto.account_name,
                balance=request_dto.balance,
                last_balance_update=datetime.now(),
            )

            account = await self.account_repository.create(account)

        diff = request_dto.balance - account.balance
        state = request_dto.state
        if account.is_balance_fixed:
            state = self.__get_state_if_balance_is_fixed(
                account, diff, request_dto.state
            )

        balance_change = BalanceChange(
            account_id=account.id,
            state_raw=request_dto.state.value,
            state=state,
            balance=request_dto.balance,
            balance_diff=diff,
        )

        account.balance = request_dto.balance
        account.is_active = request_dto.state != BalanceChangeState.SHUTDOWN
        # Если статус в списке - фиксируем баланс до следующего обновления
        if request_dto.state in [BalanceChangeState.LOCK, BalanceChangeState.SHUTDOWN]:
            account.is_balance_fixed = True

        balance_change = await self.balance_change_repository.create(balance_change)
        await self.account_repository.update(account)

        return BalanceChangeResponse.model_validate(balance_change)

    def __get_state_if_balance_is_fixed(
        self, account: Account, diff: float, state_raw: str
    ) -> BalanceChangeState:
        if diff == 0:
            if not account.is_active:
                # Лок баланса произошел по причине остановки бота - снимаем фикс
                account.is_balance_fixed = False

            # Фикс должен остаться, если аккаунт был активный

            # Если баланс не изменился - не произошло ни пополнения, ни снятия
            return state_raw  # type: ignore

        if state_raw == BalanceChangeState.UPDATE:
            # снимаем фикс с баланса если это регулярное обновление
            account.is_balance_fixed = False

        if diff < 0:
            # Если баланс уменьшился - снятие
            return BalanceChangeState.WITHDRAW

        # Если баланс увеличился - поплнение
        return BalanceChangeState.DEPOSIT
