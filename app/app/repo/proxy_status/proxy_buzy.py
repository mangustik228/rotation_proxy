from app.db_redis import REDIS
from loguru import logger


class ProxyBuzy:
    prefix = "busy_"

    @classmethod
    async def add(cls, id: int, expire: int = 300):
        '''Добавить прокси в "Занятые"'''
        await REDIS.set(f"{cls.prefix}{id}", 1, ex=expire)
        logger.info(f"proxy {id} is buzy")

    @classmethod
    async def free(cls, id: int):
        '''Освобождает прокси'''
        await REDIS.delete(f"{cls.prefix}{id}")
        logger.info(f"proxy {id} is free")

    @classmethod
    async def get_all(cls):
        """Получить все занятые прокси"""
        result: list[bytes] = await REDIS.keys(f"{cls.prefix}*")
        return [i.decode("utf-8") for i in result]

    @classmethod
    async def is_not_free(cls, id: int):
        '''Проверить являеться прокси занятой. 
        Если занята - возвращает True'''
        result = await REDIS.get(f"{cls.prefix}{id}")
        return result is not None

    @classmethod
    async def get(cls, id: int):
        '''Получить "занятую прокси по id"'''
        return await REDIS.get(f"{cls.prefix}{id}")
