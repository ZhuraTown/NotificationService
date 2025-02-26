import asyncio
import logging

from config import settings, NOTIFICATIONS_CHANNEL_NAME
from pub_sub.pub import publisher
from queues.consumer import RabbitMQConsumer
from queues.handlers import PriorityMessageHandler

logger = logging.getLogger(__name__)


async def main():
    consumer = RabbitMQConsumer(
                user=settings.rabbitmq.user,
                password=settings.rabbitmq.password,
                host=settings.rabbitmq.host,
                port=settings.rabbitmq.port,
            )
    await consumer.start()
    logger.info("Starting consumer")
    await consumer.consume(
        settings.queue.priority_queue_name,
        PriorityMessageHandler(publisher=publisher, channel_name=NOTIFICATIONS_CHANNEL_NAME),
        arguments={"x-max-priority": 10}
    )
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        ...
    finally:
        logger.info("Closing connection")
        await consumer.close()


if __name__ == "__main__":
    try:
        print('Starting consumer')
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
        print('Shutdown consumer')
