from pydantic import field_validator, model_validator

from common.enums import NotificationEventType
from dto.base import BaseDTO
from dto.user import UserRead
from datetime import datetime


class NotificationRead(BaseDTO):
    id: int
    type: str
    content: str
    author: UserRead
    created_at: datetime


class NotificationReadSubscriber(NotificationRead):
    recipient_id: int | None = None


class NotificationPaginator(BaseDTO):
    limit: int
    offset: int


class NotificationEventSchema(BaseDTO):
    type: NotificationEventType
    data: NotificationPaginator | None = None

    @model_validator(mode="after")
    @classmethod
    def validate_data(cls, data: 'NotificationEventSchema'):
        if data.type == NotificationEventType.GET_NOTIFICATIONS and not data.data:
            raise ValueError("field data is required when type is GET_NOTIFICATIONS")
        return data


