from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.balance_change import BalanceChange


class BalanceChangeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_account_id(
        self, account_id: UUID, date_from: datetime | None, date_to: datetime | None
    ) -> Sequence[BalanceChange]:
        stmt = select(BalanceChange).where(BalanceChange.account_id == account_id)
        if date_from:
            stmt = stmt.where(BalanceChange.created_at >= date_from)
        if date_to:
            stmt = stmt.where(BalanceChange.created_at < date_to)

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def create(self, balance_change: BalanceChange) -> BalanceChange:
        self.session.add(balance_change)
        await self.session.flush()
        await self.session.refresh(balance_change)

        return balance_change

    async def update(self, balance_change: BalanceChange) -> BalanceChange:
        await self.session.merge(balance_change)
        await self.session.flush()
        await self.session.refresh(balance_change)

        return balance_change
