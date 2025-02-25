from typing import TYPE_CHECKING

from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums import MessageType

from db.orm import Base
from db.orm.base import DateTimeMixin

if TYPE_CHECKING:
    from db.orm import User


class Message(
    Base,
    DateTimeMixin,
):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[MessageType] = mapped_column(Enum(MessageType))
    content: Mapped[str]
    recipient_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True, default=None)

    author_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship("User", back_populates="messages", foreign_keys=[author_id])
    # recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id])

    def __repr__(self) -> str:
        return (f"<Message id: {self.id}"
                f" type: {self.type}"
                f" author:{self.author_id}"
                f">")