from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

load_dotenv()


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")


class DBSettings(ConfigSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    @property
    def postgres_dsn(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)


class RedisSettings(ConfigSettings):
    redis_host: str = "localhost"
    redis_user: str = ""
    redis_password: str = ""
    redis_port: int = 6379

    @property
    def redis_dsn(self) -> str:
        if self.redis_user and self.redis_password:
            return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/1"
        return f"redis://{self.redis_host}:{self.redis_port}/1"


class RabbitMQSettings(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix='RM_')
    user: str = "user"
    password: str = "password"
    host: str = "host"
    port: int = 5672


class AuthSettings(ConfigSettings):
    secret_key: str = "secret_key"


class QueueSettings(ConfigSettings):
    priority_queue_name: str = "priority_queue_name"


class Settings(
    ConfigSettings
):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    queue: QueueSettings = QueueSettings()


settings = Settings()

NOTIFICATIONS_CHANNEL_NAME = "notifications_channel"
