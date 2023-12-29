import pytest
from utils import ProxyBuilder

import app.repo as R
from app.db_redis import REDIS


@pytest.fixture()
async def insert_5_proxy_to_change(sql_clear):
    builder = ProxyBuilder()
    for i in range(1, 6):
        builder.set_server(f"100.100.100.{i}")
        data = builder.build_to_repo()
        await R.Proxy.add_one(**data)
    await R.ParsedService.add_one(name="example-service")
    await REDIS.flushdb()
    yield
    await REDIS.flushdb()
