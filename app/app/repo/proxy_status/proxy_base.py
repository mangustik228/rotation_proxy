from app.db_redis import REDIS
from loguru import logger


class ProxyRedisBase:
    prefix = "busy_"

    @classmethod
    async def is_not_free(cls, id: int):
        '''Проверить являеться прокси занятой. 
        Если занята - возвращает True'''
        result = await REDIS.keys(f"*_{id}")
        return bool(result)
