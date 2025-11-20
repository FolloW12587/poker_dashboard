from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.account import Account


class AccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[Account]:
        result = await self.session.execute(select(Account).order_by(Account.name))

        return result.scalars().all()

    async def get_by_id(self, user_id: UUID) -> Account | None:
        stmt = select(Account).where(Account.id == user_id).limit(1)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def create(self, user: Account) -> Account:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update(self, user: Account) -> Account:
        await self.session.merge(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user
