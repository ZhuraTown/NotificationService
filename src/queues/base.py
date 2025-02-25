import logging
from abc import abstractmethod, ABC
from asyncio import AbstractEventLoop
from dataclasses import dataclass

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage

logger = logging.getLogger(__name__)


class OnMessageHandlerAbstract(ABC):

    @abstractmethod
    def on_message(self, message: AbstractIncomingMessage) -> any: ...


@dataclass
class RabbitMQBase:
    user: str
    password: str
    host: str
    port: str | int
    loop: AbstractEventLoop | None = None

    async def _connect(self):
        try:
            self.connection = await connect_robust(
                host=self.host,
                port=self.port,
                login=self.user,
                password=self.password,
                loop=self.loop
            )
            self.channel = await self.connection.channel()
        except Exception as e:
            logger.critical(f"Cannot create connection for RabbitMq. Error: {e}")
            data = dict(host=self.host, port=self.port, user=self.user, password=self.password)
            logger.critical(f"Connect data.host: {data}")
            raise e
        else:
            logger.info("Connection success")

    async def start(self):
        await self._connect()

    async def close(self):
        from asyncio import sleep
        await sleep(3)
        await self.connection.close()
