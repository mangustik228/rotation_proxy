from redis.asyncio import Redis
from app.config import settings

REDIS = Redis.from_url("redis://db_redis", password=settings.redis.password)
