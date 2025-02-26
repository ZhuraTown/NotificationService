import json

from aio_pika.abc import AbstractIncomingMessage

from db.database import db
from db.orm import Message
from db.repo.message import MessageRepository
from dto.notifications import NotificationReadSubscriber
from pub_sub.pub import RedisPublisher
from queues.base import OnMessageHandlerAbstract


class PriorityMessageHandler(OnMessageHandlerAbstract):

    def __init__(self, publisher: RedisPublisher, channel_name: str):
        self.channel_name = channel_name
        self.publisher = publisher

    def _validate_data(self, message_body: dict) -> Message:
        return Message(
            type=message_body['type'],
            content=message_body['content'],
            recipient_id=message_body.get('recipient'),
            author_id=message_body['author']
        )

    async def on_message(self, message: AbstractIncomingMessage):
        async with message.process():
            msg_body = json.loads(message.body)
            message = self._validate_data(msg_body)
            async with db.session() as session:
                msg = await MessageRepository.create_for_user(
                    session, message
                )
                await session.commit()
                msg = await MessageRepository.get_message(session, msg.id)
            await self.publisher.publish(
                    self.channel_name, NotificationReadSubscriber.parse_obj(msg).model_dump(mode='json')
                )
