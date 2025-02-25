from queues.producer import RabbitMQProducer, producer


async def get_producer() -> RabbitMQProducer:
    return producer
