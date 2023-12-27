from app.db_redis import REDIS
from loguru import logger


class ProxyBlocked:
    prefix = "blocked_"

    @classmethod
    async def add(cls, proxy_id: int, service: str, expire: int = 300):
        '''Добавить прокси в "Занятые"'''
        await REDIS.set(f"{cls.prefix}{service}_{proxy_id}", 1, ex=expire)
        logger.info(f"proxy {proxy_id} is blocked")

    @classmethod
    async def free(cls, proxy_id: int, service: str):
        '''Освобождает заблоченную прокси по определенному сервису'''
        await REDIS.delete(f"{cls.prefix}{service}_{proxy_id}")
        logger.info(f"proxy {proxy_id} is free from blocked list")

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
    async def is_free(cls, proxy_id: int, parsed_service: str):
        '''Проверить являеться прокси заблокированной в каком то сервисе
        Если свободен возвращает True'''
        result = await REDIS.get(f"{cls.prefix}{parsed_service}_{proxy_id}")
        return result is None

    @classmethod
    async def where_id_blocked(cls, proxy_id: int):
        '''Возвращает список в каком сервисе заблокирован данный id, если нигде, то []'''
        result: list[bytes] = await REDIS.keys(f'{cls.prefix}*_{proxy_id}')
        return [i.decode("utf-8").split("_")[1] for i in result]

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
            if "blocked_" not in key:
                continue
            item = {}
            _, item["service"], item["id"] = key.split("_")
            item["expire"] = value
            logger.info(item)
            result.append(item)
        return result
