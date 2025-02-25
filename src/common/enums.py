from enum import Enum


class MessageType(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class NotificationEventType(str, Enum):
    GET_NOTIFICATIONS = "get_notifications"
    MARK_ALL_AS_READ = "mark_all_as_read"
