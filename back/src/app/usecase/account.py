from uuid import UUID

from app.dto.account import AccountResponse
from app.usecase.errors import NotFoundError
from infra.db.account import AccountRepository


class AccountUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
    ):
        self.account_repository = account_repository

    async def get_account(self, account_id: UUID) -> AccountResponse:
        account = await self.account_repository.get_by_id(account_id)
        if not account:
            raise NotFoundError(f"Account with id {account_id} not found")

        return AccountResponse.model_validate(account)

    async def get_accounts(self) -> list[AccountResponse]:
        accounts = await self.account_repository.get_all()

        return [AccountResponse.model_validate(account) for account in accounts]
