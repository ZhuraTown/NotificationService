from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions import ToClientException
from db.orm import User
from db.repo.user import UserRepository
from dto.user import CreateUser, LoginCreate
from service.password import hash_password, verify_password


class UserService:

    @classmethod
    async def create_user(cls, user_data: CreateUser, session: AsyncSession) -> User:
        if await UserRepository.get_user_by_username(session, user_data.username):
            raise ToClientException(errors=f"Username with name {user_data.username} already exists")
        new_user = User(**user_data.model_dump(mode='json'))
        new_user.password = hash_password(user_data.password)
        created_user = await UserRepository.create_user(session, new_user)
        await session.commit()
        return created_user

    @classmethod
    async def auth_user(
            cls,
            credentials: LoginCreate,
            session: AsyncSession
    ) -> User:
        found_user = await UserRepository.get_user_by_username(session, credentials.username)
        if not found_user or not verify_password(credentials.password, found_user.password):
            raise ToClientException(errors="Bad credentials")
        return found_user

    @classmethod
    async def get_user_by_id(
            cls,
            user_id: str,
            session: AsyncSession,
    ) -> User | None:
        return await UserRepository.get_user_by_id(session, user_id)

    @classmethod
    async def list_users(cls, session: AsyncSession):
        return await UserRepository.get_users(session)

