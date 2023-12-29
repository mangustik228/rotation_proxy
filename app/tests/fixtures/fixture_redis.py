import pytest

from app.db_redis import REDIS


@pytest.fixture()
async def redis_insert_blocked_10(redis_clear):
    for i in range(1, 5):
        await REDIS.set(f"blocked_test-service_{i}", 1)
        await REDIS.set(f"blocked_test-service-2_{i}", 1)
    yield


@pytest.fixture()
async def redis_clear():
    await REDIS.flushdb()
    yield
    await REDIS.flushdb()
