from uuid import UUID

from app.dto.account import AccountResponse
from app.usecase.errors import InvalidInputError, NotFoundError
from infra.db.account import AccountRepository


from infra.utils.log import logger


class AccountUseCase:
    def __init__(
        self,
        user_repository: AccountRepository,
    ):
        self.user_repository = user_repository

    async def get_user(self, user_id: UUID) -> AccountResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")

        return AccountResponse.model_validate(user)
