from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.orm import User


class UserRepository:

    @classmethod
    async def get_user_by_username(
            cls,
            session: AsyncSession,
            username: str
    ) -> User | None:
        result = await session.scalar(select(User).where(User.username == username))
        return result

    @classmethod
    async def get_user_by_id(
            cls,
            session: AsyncSession,
            user_id: int
    ) -> User | None:
        result = await session.scalar(select(User).where(User.id == user_id))
        return result

    @classmethod
    async def create_user(
            cls,
            session: AsyncSession,
            user: User
    ):
        session.add(user)
        return user

    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[User]:
        results = await session.scalars(select(User))
        return results.all()


