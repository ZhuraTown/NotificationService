import logging
from collections import defaultdict

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.websockets import WebSocket

from common.enums import NotificationEventType
from db.orm import User
from dto.notifications import NotificationRead, NotificationEventSchema
from service.messages import MessageService

logger = logging.getLogger(__name__)


class NotificationManager:

    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(
            self,
            websocket: WebSocket,
            current_user: User,
            session: AsyncSession,
    ):
        await websocket.accept()
        self.active_connections[current_user.id].add(websocket)
        notifications = await MessageService.get_messages(session, current_user.id, limit=30, offset=0)
        data = {
            "objects": [
                NotificationRead.parse_obj(n).model_dump(mode='json') for n in notifications
            ]
        }
        await self._send_message(data, status=status.WS_1000_NORMAL_CLOSURE, websocket=websocket)

    @staticmethod
    async def _send_message(data: dict, status: int, websocket):
        data = {'status': status, 'data': data}
        await websocket.send_json(data)

    async def receive_message(self,
                              data: dict,
                              websocket: WebSocket,
                              user: User,
                              session: AsyncSession,
                              ):
        try:
            event: NotificationEventSchema = NotificationEventSchema.model_validate(data)
        except ValidationError as e:
            logger.warning(f"Invalid json schema format was obtained from: {e}")
            await self._send_message(
                data={'detail': f'Invalid json schema format for event'},
                status=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
                websocket=websocket
            )
        else:
            await self.action_by_event(event, user, websocket, session)

    # async def broadcast_message(self, message: dict):
    #     for user_id, connection_data in self.active_connections.items():
    #         connection_data: [WebSocket, User]
    #         websocket, user = connection_data
    #         await self._send_message(message, status=1000, websocket=websocket)

    async def disconnect(self, current_user: User, websocket: WebSocket):
        self.active_connections[current_user.id].discard(websocket)
        if not self.active_connections[current_user.id]:
            del self.active_connections[current_user.id]

    async def action_by_event(
            self,
            event: NotificationEventSchema,
            user: User,
            websocket: WebSocket,
            session: AsyncSession,
    ):
        match event.type:
            case NotificationEventType.GET_NOTIFICATIONS:
                notifications = await MessageService.get_messages(
                    session, user.id, limit=event.data.limit, offset=event.data.offset
                )
                data = {
                    "objects": [
                        NotificationRead.parse_obj(n).model_dump(mode='json') for n in notifications
                    ]
                }
                await self._send_message(data, status=1000, websocket=websocket)
            case NotificationEventType.MARK_ALL_AS_READ:
                ...

    async def receive_json(
            self,
            websocket: WebSocket
    ) -> dict:
        try:
            return await websocket.receive_json()
        except Exception as e:
            logger.warning(f"Invalid data: {e}")
            await self._send_message(
                data={'detail': f'Invalid json schema format for event'},
                status=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
                websocket=websocket
            )

