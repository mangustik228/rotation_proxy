import pytest
from app.db_redis import REDIS


@pytest.fixture()
async def clear_redis():
    await REDIS.flushdb()
    yield
    await REDIS.flushdb()


@pytest.fixture()
async def insert_blocked():
    await REDIS.flushdb()
    for i in range(1, 5):
        await REDIS.set(f"blocked_test-service_{i}", 1)
        await REDIS.set(f"blocked_test-service-2_{i}", 1)
    yield
    await REDIS.flushdb()
