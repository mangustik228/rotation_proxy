import json
import os
from datetime import datetime

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import insert

import app.models as M
from app.db_postgres import async_session


@pytest.fixture()
async def sql_clear():
    assert os.getenv("MODE") == "TEST", "base is not test"
    yield
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_section_option("logger_alembic", "level", "WARN")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture
async def sql_insert_parsed_service(sql_insert_10_proxies):
    async with async_session() as session:
        service = M.ParsedService(name="example-service")
        session.add(service)
        await session.commit()
    yield


@pytest.fixture
async def sql_insert_2_parsed_services(sql_insert_10_proxies):
    async with async_session() as session:
        parsed_service_1 = M.ParsedService(name="example-service")
        parsed_service_2 = M.ParsedService(name="example-service-2")
        session.add(parsed_service_1)
        session.add(parsed_service_2)
        await session.commit()
    yield


@pytest.fixture
async def sql_insert_3_errors(sql_insert_10_proxies):
    async with async_session() as session:
        service = M.ParsedService(name="example-service")
        for _ in range(3):
            error = M.Error(reason="cloudflare", proxy_id=1, sleep_time=5)
            error.parsed_service = service
            session.add(error)
        await session.commit()
    yield


@pytest.fixture
async def sql_insert_10_proxies(sql_clear):
    with open(f'tests/src/proxies.json', "r") as file:
        data = json.load(file)
    for datum in data:
        datum['expire'] = datetime.fromisoformat(datum['expire'])
    async with async_session() as session:
        stmt = insert(M.Proxy).values(data)
        await session.execute(stmt)
        await session.commit()
    yield
