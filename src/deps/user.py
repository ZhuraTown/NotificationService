from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from deps.db import get_session
from service.password import ALGORITHM, SECRET_KEY, security
from service.user import UserService


async def user_service():
    return UserService


async def get_current_user(
        session: Annotated[AsyncSession,  Depends(get_session)],
        token: HTTPBearer = Depends(security),
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("id")
        expire: str = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise HTTPException(status_code=401, detail="The token expired")
        user = await UserService.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
