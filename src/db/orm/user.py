from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.orm.base import Base, DateTimeMixin


if TYPE_CHECKING:
    from db.orm import Message


class User(
    Base,
    DateTimeMixin
):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="author", foreign_keys="[Message.author_id]"
    )
