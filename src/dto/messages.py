from common.enums import MessageType
from dto.base import BaseDTO


class CreateMessage(BaseDTO):
    type: MessageType
    content: str
    recipient: int | None = None


class MessageCreated(BaseDTO):
    info: str


class MessageQueue(CreateMessage):
    author: int

