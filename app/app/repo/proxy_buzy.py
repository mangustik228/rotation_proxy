from app.db_redis import REDIS
from loguru import logger


class ProxyBuzy:
    prefix = "busy_"

    @classmethod
    async def add(cls, id: int, expire: int = 300):
        await REDIS.set(f"{cls.prefix}{id}", 1, ex=expire)
        logger.info("proxy {id} is buzy")

    @classmethod
    async def free(cls, id: int):
        await REDIS.delete(f"{cls.prefix}{id}")
        logger.info("proxy {id} is free")

    @classmethod
    async def get_all(cls):
        return await REDIS.keys(f"{cls.prefix}*")

    @classmethod
    async def is_busy(cls, id: int):
        result = await REDIS.get(f"{cls.prefix}{id}")
        return result is not None

    @classmethod
    async def get(cls, id: int):
        return await REDIS.get(f"{cls.prefix}{id}")
