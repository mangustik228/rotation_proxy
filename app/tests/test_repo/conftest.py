import pytest
from app.db_redis import REDIS


@pytest.fixture(autouse=True, scope="function")
async def clear_redis():
    await REDIS.flushdb()
    yield
    await REDIS.flushdb()
