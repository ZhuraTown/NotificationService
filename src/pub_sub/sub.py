import asyncio
import redis.asyncio as redis

from db.redis import redis_db


class RedisSubscriber:

    def __init__(self, r: redis.Redis):
        self.r = r
        self.pubsub = self.r.pubsub()

    async def subscribe(self, channel_name: str, **kwargs):
        await self.pubsub.subscribe(channel_name, **kwargs)

    async def unsubscribe(self, channel_name: str):
        await self.pubsub.unsubscribe(channel_name)

    async def listen_messages(self, timeout: int | None = 1):
        while True:
            message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=timeout)
            if message:
                print(f"Received message: {message}")
                yield message

    async def close(self):
        await self.r.close()


subscriber = RedisSubscriber(redis_db)


# async def main():
#     CHANNEL_NAME = "notifications"
#
#     await subscriber.subscribe(CHANNEL_NAME)
#
#     async for msg in subscriber.listen_messages():
#         print("Получено сообщение, что-то с ним типа делаю ", msg)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())