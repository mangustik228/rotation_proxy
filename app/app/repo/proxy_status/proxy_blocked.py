from app.db_redis import REDIS
from loguru import logger


class ProxyBlocked:
    prefix = "blocked_"

    @classmethod
    async def add(cls, id: int, service: str, expire: int = 300):
        '''Добавить прокси в "Занятые"'''
        await REDIS.set(f"{cls.prefix}{service}_{id}", 1, ex=expire)
        logger.info(f"proxy {id} is buzy")

    @classmethod
    async def free(cls, id: int, service: str):
        '''Освобождает прокси'''
        await REDIS.delete(f"{cls.prefix}{service}_{id}")
        logger.info(f"proxy {id} is free")

    @classmethod
    async def get_all(cls):
        """Получить все заблокированные прокси"""
        result: list[bytes] = await REDIS.keys(f"{cls.prefix}*")
        return [i.decode("utf-8") for i in result]

    @classmethod
    async def get_all_by_service(cls, service: str):
        '''Получить все заблокированные прокси для определенного сервиса'''
        result: list[bytes] = await REDIS.keys(f"{cls.prefix}{service}_*")
        return [i.decode("utf-8") for i in result]

    @classmethod
    async def is_blocked_by_service(cls, id: int, service: str):
        '''Проверить являеться прокси заблокированной в каком то сервисе'''
        result = await REDIS.get(f"{cls.prefix}{service}_{id}")
        return result is not None

    @classmethod
    async def where_id_blocked(cls, id: int):
        '''Возвращает список в каком сервисе заблокирован данный id, если нигде, то []'''
        result: list[bytes] = await REDIS.keys(f'{cls.prefix}*_{id}')
        return [i.decode("utf-8").split("_")[1] for i in result]

    # @classmethod
    # async def get(cls, id: int):
    #     '''Получить "занятую прокси по id"'''
    #     return await REDIS.get(f"{cls.prefix}*_{id}")
