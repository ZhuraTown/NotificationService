import json
import redis.asyncio as redis
from db.redis import redis_db


class RedisPublisher:

    def __init__(self, r: redis.Redis):
        self.r = r
        self.pubsub = r.pubsub()

    async def publish(self, channel_name: str, message: any):
        if isinstance(message, dict):
            message = json.dumps(message)
        await self.r.publish(channel_name, message)

    async def close(self):
        await self.r.close()


publisher = RedisPublisher(redis_db)
#
#
# import asyncio
# from config import NOTIFICATIONS_CHANNEL_NAME
#
#
# async def main():
#     CHANNEL_NAME = NOTIFICATIONS_CHANNEL_NAME
#
#     def msg_generator(n: int):
#         for i in range(n):
#             yield {"id": i, "data": "Hello World!"}
#
#     await asyncio.sleep(1)
#     for msg in msg_generator(100):
#         await asyncio.sleep(1)
#         print("publishing", msg)
#         await publisher.publish(NOTIFICATIONS_CHANNEL_NAME, msg)
#     await publisher.publish(NOTIFICATIONS_CHANNEL_NAME, "STOP")
#     await asyncio.sleep(1)
#     await publisher.close()
#
# if __name__ == "__main__":
#     asyncio.run(main())
