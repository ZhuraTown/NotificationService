from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.orm import User
from deps.db import get_session
from deps.message import message_service
from deps.producer import get_producer
from deps.user import get_current_user
from dto.messages import CreateMessage, MessageCreated
from queues.producer import RabbitMQProducer
from service.messages import MessageService

router = APIRouter(prefix='/messages', tags=['messages'])


@router.post(
    "",
    response_model=MessageCreated,
)
async def create_message(
        new_message: CreateMessage,
        service: Annotated[MessageService, Depends(message_service)],
        session: Annotated[AsyncSession, Depends(get_session)],
        producer: Annotated[RabbitMQProducer, Depends(get_producer)],
        author: Annotated[User, Depends(get_current_user)],
):
    await service.create_message(session, new_message, author.id, producer, settings.queue.priority_queue_name)
    return MessageCreated(info="message added to queue")
