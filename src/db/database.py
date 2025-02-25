import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            settings.db.postgres_dsn,
            echo=False,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            autoflush=True,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[type[AsyncSession], None]:
        async with self.session_factory() as session:
            try:
                yield session
            except DatabaseError as e:
                logging.error(f"Transaction failed: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()


db = Database()