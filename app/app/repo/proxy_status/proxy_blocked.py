from app.db_redis import REDIS
from loguru import logger


class ProxyBlocked:
    prefix = "blocked_"

    @classmethod
    async def add(cls, id: int, service: str, expire: int = 300):
        '''Добавить прокси в "Занятые"'''
        await REDIS.set(f"{cls.prefix}{service}_{id}", 1, ex=expire)
        logger.info(f"proxy {id} is blocked")

    @classmethod
    async def free(cls, id: int, service: str):
        '''Освобождает заблоченную прокси по определенному сервису'''
        await REDIS.delete(f"{cls.prefix}{service}_{id}")
        logger.info(f"proxy {id} is free from blocked list")

    @classmethod
    async def get_all(cls):
        """Получить все заблокированные прокси"""
        result: list[bytes] = await REDIS.keys(f"{cls.prefix}*")
        return [i.decode("utf-8") for i in result]

    @classmethod
    async def get_all_by_service(cls, parsed_service: str):
        '''Получить все заблокированные прокси для определенного сервиса'''
        result: list[bytes] = await REDIS.keys(f"{cls.prefix}{parsed_service}_*")
        return [i.decode("utf-8") for i in result]

    @classmethod
    async def is_not_free(cls, id: int, parsed_service: str):
        '''Проверить являеться прокси заблокированной в каком то сервисе
        Если заблокирован - возвращает True'''
        result = await REDIS.get(f"{cls.prefix}{parsed_service}_{id}")
        return result is not None

    @classmethod
    async def where_id_blocked(cls, id: int):
        '''Возвращает список в каком сервисе заблокирован данный id, если нигде, то []'''
        result: list[bytes] = await REDIS.keys(f'{cls.prefix}*_{id}')
        return [i.decode("utf-8").split("_")[1] for i in result]
