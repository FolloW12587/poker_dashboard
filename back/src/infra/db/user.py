from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id).limit(1)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def get_by_name(self, user_name: str) -> User | None:
        stmt = select(User).where(User.username == user_name).limit(1)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update(self, user: User) -> User:
        await self.session.merge(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user
