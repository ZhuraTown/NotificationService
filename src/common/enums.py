from enum import Enum


class MessageType(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
