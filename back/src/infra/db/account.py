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

    async def get_by_id(self, account_id: UUID) -> Account | None:
        stmt = select(Account).where(Account.id == account_id).limit(1)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def get_by_name(self, account_name: str) -> Account | None:
        stmt = select(Account).where(Account.name == account_name).limit(1)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def create(self, account: Account) -> Account:
        self.session.add(account)
        await self.session.flush()
        await self.session.refresh(account)

        return account

    async def update(self, account: Account) -> Account:
        await self.session.merge(account)
        await self.session.flush()
        await self.session.refresh(account)

        return account
