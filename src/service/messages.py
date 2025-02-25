import logging

from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions import ToClientException
from aio_pika import Message

from common.priorities import QUEUE_MESSAGES_PRIORITY
from db.repo.user import UserRepository
from dto.messages import CreateMessage, MessageQueue
from queues.producer import RabbitMQProducer


logger = logging.getLogger(__name__)


class MessageService:

    @classmethod
    async def create_message(
            cls,
            session: AsyncSession,
            message_data: CreateMessage,
            author: int,
            # todo: add later
            producer: RabbitMQProducer,
            queue_name: str
    ):
        if recipient_id := message_data.recipient:
            if not await UserRepository.get_user_by_id(session, recipient_id):
                raise ToClientException(errors=f"User({recipient_id}) not found")
        message = MessageQueue(**message_data.dict(), author=author)
        await producer.send_json_message(
            queue_name,
            message.model_dump(mode='json'),
            priority=QUEUE_MESSAGES_PRIORITY[message_data.type]
        )


async def create_message(message: Message):
    ...