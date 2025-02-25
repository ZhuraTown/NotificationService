import logging

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import db


async def get_session() -> AsyncSession:
    async with db.session() as session:
        try:
            yield session
        except DatabaseError as e:
            logging.error(f"Transaction failed: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()