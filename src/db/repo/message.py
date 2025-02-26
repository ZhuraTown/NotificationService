from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.orm import Message


class MessageRepository:

    @classmethod
    async def create_for_user(
            cls,
            session: AsyncSession,
            message: Message
    ) -> Message | None:
        session.add(message)
        return message

    @classmethod
    async def get_message(
            cls,
            session: AsyncSession,
            msg_id: int
    ) -> Message | None:
        return await session.scalar(
            select(Message)
            .where(Message.id == msg_id)
            .options(joinedload(Message.author))
        )

    @classmethod
    async def create_for_all(
            cls,
            session: AsyncSession,
            messages: list[Message]
    ):
        session.add_all(messages)
        return messages

    @classmethod
    async def list_messages(
            cls,
            session: AsyncSession,
            user_id: int,
            limit: int,
            offset: int,
    ) -> list[Message]:
        query = (
            select(Message).where(
                or_(
                    Message.recipient_id == user_id,
                    Message.recipient_id.is_(None)
                )
            )
            .options(
                joinedload(Message.author)
            )
            .order_by(desc(Message.created_at))
            .limit(limit)
            .offset(offset)
        )
        return (await session.scalars(query)).all()


