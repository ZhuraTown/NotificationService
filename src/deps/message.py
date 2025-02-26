from api.managers.notification import manager_notifications, NotificationManager
from service.messages import MessageService


async def message_service():
    return MessageService


async def get_notifications_manager() -> NotificationManager:
    return manager_notifications
