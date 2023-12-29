import pytest
from utils import ProxyBuilder

import app.repo as R
from app.db_redis import REDIS

from .functions import update_db


@pytest.fixture()
async def insert_5_proxy_to_change():
    await update_db()
    builder = ProxyBuilder()
    for i in range(1, 6):
        builder.set_server(f"100.100.100.{i}")
        data = builder.build_to_repo()
        await R.Proxy.add_one(**data)
    await R.ParsedService.add_one(name="example-service")
    await REDIS.flushdb()
    yield
    await update_db()
    await REDIS.flushdb()


@pytest.fixture()
async def insert_blocked():
    await REDIS.flushdb()
    for i in range(1, 5):
        await REDIS.set(f"blocked_test-service_{i}", 1)
        await REDIS.set(f"blocked_test-service-2_{i}", 1)
    yield
    await REDIS.flushdb()


@pytest.fixture()
async def clear_redis():
    await REDIS.flushdb()
    yield
    await REDIS.flushdb()
