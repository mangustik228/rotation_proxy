import pytest
from app.db_redis import REDIS


@pytest.fixture(autouse=True, scope="function")
async def clear_redis():
    await REDIS.flushdb()
    yield
    await REDIS.flushdb()


@pytest.fixture()
async def insert_blocked():
    for i in range(1, 5):
        await REDIS.set(f"blocked_test-example_{i}", 1)
        await REDIS.set(f"blocked_test-example-2_{i}", 1)
