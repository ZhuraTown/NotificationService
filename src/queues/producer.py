import json
from aio_pika import Message, DeliveryMode
from aio_pika.abc import AbstractExchange

from src.config import settings
from src.queues.base import RabbitMQBase


class RabbitMQProducer(RabbitMQBase):
    exchange: AbstractExchange

    async def start(self):
        await super().start()

    async def send_json_message(self, queue_name: str, data: dict, priority: int | None = None):
        body = json.dumps(data).encode()
        message = Message(
            body=body,
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,
            priority=priority
        )
        await self.channel.default_exchange.publish(
            message,
            routing_key=queue_name,
        )


producer = RabbitMQProducer(
        user=settings.rabbitmq.user,
        password=settings.rabbitmq.password,
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
    )
