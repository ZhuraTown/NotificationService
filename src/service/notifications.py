import json

from pydantic import ValidationError

from api.managers.notification import NotificationManager
from dto.notifications import NotificationRead, NotificationReadSubscriber
from pub_sub.sub import RedisSubscriber


def convert_data_to_msg(data: any) -> NotificationReadSubscriber | None:
    try:
        return NotificationReadSubscriber.parse_raw(data)
    except ValidationError as e:
        print("Error convert_data", e)


async def broadcast_new_notifications(
        channel_name: str,
        sub: RedisSubscriber,
        ws_manager: NotificationManager
):
    await sub.subscribe(channel_name)
    async for message in sub.listen_messages():
        message = convert_data_to_msg(message.get('data'))
        if not message:
            continue
        await ws_manager.broadcast_message(message)

    await sub.unsubscribe(channel_name)