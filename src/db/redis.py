from config import settings
import redis.asyncio as redis


redis_db = redis.from_url(settings.redis.redis_dsn, decode_responses=True)