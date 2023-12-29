import hashlib
import pickle
from functools import wraps

from app.db_redis import REDIS


def redis_cache(func: callable):
    @wraps(func)
    async def inner(*args, **kwargs):
        key = hashlib.md5((func.__name__ + str(args) +
                          str(kwargs)).encode()).hexdigest()
        result = await REDIS.get(key)
        if result:
            return pickle.loads(result)
        result = await func(*args, **kwargs)
        await REDIS.set(key, pickle.dumps(result), ex=5)
        return result
    return inner
