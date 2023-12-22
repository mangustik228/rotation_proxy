from app.db_redis import REDIS
from loguru import logger


class ProxyBase:
    prefix = "busy_"

    @classmethod
    async def add(cls, id: int, expire: int = 300):
        '''Добавить прокси в "Занятые"'''
        await REDIS.set(f"{cls.prefix}{id}", 1, ex=expire)
        logger.info("proxy {id} is buzy")

    @classmethod
    async def free(cls, id: int):
        '''Освобождает прокси'''
        await REDIS.delete(f"{cls.prefix}{id}")
        logger.info("proxy {id} is free")

    @classmethod
    async def get_all(cls):
        """Получить все занятые прокси"""
        return await REDIS.keys(f"{cls.prefix}*")

    @classmethod
    async def is_busy(cls, id: int):
        '''Проверить являеться прокси занятой'''
        result = await REDIS.get(f"{cls.prefix}{id}")
        return result is not None

    @classmethod
    async def get(cls, id: int):
        '''Получить "занятую прокси по id"'''
        return await REDIS.get(f"{cls.prefix}{id}")
