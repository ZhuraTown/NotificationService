from sqlalchemy.ext.asyncio import AsyncSession

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
    async def create_for_all(
            cls,
            session: AsyncSession,
            messages: list[Message]
    ):
        session.add_all(messages)
        return messages
