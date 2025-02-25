from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deps.db import get_session
from deps.user import user_service, get_current_user
from dto.user import UserCreated, CreateUser, LoginCreate, JWTTokenResponse, UserRead
from service.password import create_access_token
from service.user import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '',
    response_model=UserCreated
)
async def create_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        service: Annotated[UserService, Depends(user_service)],
        user_data: CreateUser
):
    new_user = await service.create_user(user_data, session)
    return new_user


@router.get(
    "",
    response_model=list[UserRead],
    dependencies=[
        Depends(get_current_user)
    ]
)
async def list_users(
        session: Annotated[AsyncSession, Depends(get_session)],
        service: Annotated[UserService, Depends(user_service)],
):
    users = await service.list_users(session)
    return users


@router.post(
    '/login',
    response_model=JWTTokenResponse
)
async def login(
        session: Annotated[AsyncSession, Depends(get_session)],
        service: Annotated[UserService, Depends(user_service)],
        credentials: LoginCreate
):
    auth_user = await service.auth_user(credentials, session)
    return JWTTokenResponse(
        access_token=create_access_token({"id": auth_user.id})
    )

