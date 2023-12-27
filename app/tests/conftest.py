import logging
import os
from loguru import logger

if True:
    os.environ["MODE"] = "TEST"

import json
from datetime import datetime
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy import delete, insert, text
from alembic import command
from alembic.config import Config


import app.models as M
from app.db_postgres import engine, async_session
from app.main import app as fastapi_app
from app.config import settings
from tests.utils import ProxyBuilder
from app.db_redis import REDIS


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


@pytest.fixture
async def insert_parsed_service():
    async with async_session() as session:
        service = M.ParsedService(name="example-service")
        session.add(service)
        second_service = M.ParsedService(name="another")
        session.add(second_service)
        await session.commit()
        yield
    await update_db()


@pytest.fixture
async def insert_3_errors():
    async with async_session() as session:
        service = M.ParsedService(name="example-service")
        for _ in range(3):
            error = M.Error(reason="cloudflare", proxy_id=1, sleep_time=5)
            error.parsed_service = service
            session.add(error)
        await session.commit()
    yield
    await update_db()


@pytest.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(
            app=fastapi_app,
            base_url="http://test",
            headers={"X-API-Key": settings.APIKEY}
    ) as ac:
        yield ac


@pytest.fixture
async def insert_proxies_and_errors():
    ...


@pytest.fixture
async def insert_parsed_services():
    async with async_session() as session:
        parsed_service_1 = M.ParsedService(name="example-service")
        parsed_service_2 = M.ParsedService(name="example-service-2")
        session.add(parsed_service_1)
        session.add(parsed_service_2)
        await session.commit()
    yield
    await update_db()


@pytest.fixture
async def insert_proxies_10_proxies():
    await update_db()
    with open(f'tests/src/proxies.json', "r") as file:
        data = json.load(file)
    for datum in data:
        datum['expire'] = datetime.fromisoformat(datum['expire'])
    async with async_session() as session:
        stmt = insert(M.Proxy).values(data)
        await session.execute(stmt)
        await session.commit()
    yield
    await update_db()


async def update_db():
    assert os.getenv("MODE") == "TEST", "base is not test"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_section_option("logger_alembic", "level", "WARN")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    await update_db()


@pytest.fixture(scope="session", autouse=True)
def disallow_loguru_logger():
    while True:
        try:
            logger.remove(0)
        except ValueError:
            break


@pytest.fixture(scope="session", autouse=True)
def disallow_logging():
    logging.disable(logging.INFO)
    ...
# Из документации pytest


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def clear_db():
    yield
    await update_db()
