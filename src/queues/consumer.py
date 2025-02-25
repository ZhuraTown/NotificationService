from src.queues.base import RabbitMQBase, OnMessageHandlerAbstract


class RabbitMQConsumer(RabbitMQBase):

    async def consume(
            self,
            queue_name: str,
            message_handler: OnMessageHandlerAbstract,
            arguments: dict | None = None):
        queue = await self.channel.declare_queue(
            queue_name, durable=True, robust=True, arguments=arguments
        )

        await queue.consume(message_handler.on_message)