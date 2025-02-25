from common.enums import MessageType

QUEUE_MESSAGES_PRIORITY = {
    MessageType.CRITICAL: 10,
    MessageType.WARNING: 5,
    MessageType.INFO: 1,
}