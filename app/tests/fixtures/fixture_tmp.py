from unittest.mock import patch
from httpx import AsyncClient

import pytest
from fixtures.functions import update_db
from utils import ProxyBuilder

import app.repo as R
from app.db_redis import REDIS
from app.middlewares.log_middleware import LogMiddleware

from app.main import app as fastapi_app
from app.config import settings


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


async def mock_middleware_dispatch(self, request, call_next):
    return await call_next(request)


@pytest.fixture
def mock_middleware_logs():
    with patch.object(LogMiddleware, "dispatch", new=mock_middleware_dispatch) as mock_method:
        yield
