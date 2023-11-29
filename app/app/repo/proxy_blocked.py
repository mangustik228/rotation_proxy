from app.db_redis import REDIS


class ProxyBlocked:
    @classmethod
    def add(cls, service: str, proxy: dict, expire: int | None = None):
        ...

    @classmethod
    def delete(cls, service: str, proxy: dict):
        ...

    @classmethod
    def get_all_blocked_by_service(cls, service: str):
        ...

    @classmethod
    def get_all(cls):
        ...

    @classmethod
    async def exist(cls, proxy: str):
        return bool(await REDIS.get(proxy))
