from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, WebSocketException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.websockets import WebSocket

from deps.db import get_session
from service.password import ALGORITHM, SECRET_KEY, security
from service.user import UserService


async def user_service():
    return UserService


async def get_current_user_ws(
        websocket: WebSocket,
        session: Annotated[AsyncSession,  Depends(get_session)],
):
    access_token = websocket.query_params.get("access_token")
    if not access_token:
        await websocket.close(code=1008)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("id")
        expire: str = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        user = await UserService.get_user_by_id(user_id, session)
        if not user:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return user
    except JWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


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
