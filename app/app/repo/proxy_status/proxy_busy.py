from loguru import logger

from app.db_redis import REDIS


class ProxyBusy:
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
    async def is_free(cls, id: int):
        '''Проверить являеться прокси занятой.
        Если свободен возвращает True'''
        result = await REDIS.get(f"{cls.prefix}{id}")
        return result is None

    @classmethod
    async def get(cls, id: int):
        '''Получить "занятую прокси по id"'''
        return await REDIS.get(f"{cls.prefix}{id}")

    @classmethod
    async def get_all_with_expire(cls):
        keys_with_ttl = {}
        cursor = b'0'  # Инициализация курсора для SCAN
        while cursor:
            cursor, keys = await REDIS.scan(cursor)
            for key in keys:
                ttl = await REDIS.ttl(key)
                keys_with_ttl[key.decode("utf-8")] = ttl

        result = []
        for key, value in keys_with_ttl.items():
            logger.info(f"{key = } {value = }")
            if "busy_" not in key:
                continue
            item = {}
            item["id"] = key.split("_")[-1]
            item["expire"] = value
            logger.info(item)
            result.append(item)
        return result
