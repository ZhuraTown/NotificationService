from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.managers.notification import NotificationManager
from db.orm import User
from deps.db import get_session
from deps.message import get_notifications_manager
from deps.user import get_current_user_ws

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.websocket(
    ""
)
async def list_notifications(
        websocket: WebSocket,
        user: Annotated[User, Depends(get_current_user_ws)],
        session: Annotated[AsyncSession, Depends(get_session)],
        ws_manager: Annotated[NotificationManager, Depends(get_notifications_manager)]
):
    await ws_manager.connect(websocket, user, session)
    try:
        while True:
            data = await ws_manager.receive_json(websocket)
            if data:
                await ws_manager.receive_message(data, websocket, user, session)
    except WebSocketDisconnect:
        await ws_manager.disconnect(user, websocket)