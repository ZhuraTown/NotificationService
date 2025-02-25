from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.managers.notification import NotificationManager
from db.orm import User
from deps.db import get_session
from deps.user import get_current_user_ws

router = APIRouter(prefix='/notifications', tags=['notifications'])

manager_notifications = NotificationManager()


@router.websocket(
    ""
)
async def list_notifications(
        websocket: WebSocket,
        user: Annotated[User, Depends(get_current_user_ws)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    await manager_notifications.connect(websocket, user, session)
    try:
        while True:
            data = await manager_notifications.receive_json(websocket)
            if data:
                await manager_notifications.receive_message(data, websocket, user, session)
    except WebSocketDisconnect:
        await manager_notifications.disconnect(user, websocket)