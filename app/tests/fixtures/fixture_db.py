import json
from datetime import datetime

import pytest
from sqlalchemy import insert

import app.models as M
from app.db_postgres import async_session

from .functions import update_db


@pytest.fixture()
async def clear_db():
    await update_db()
    yield
    await update_db()


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    await update_db()


@pytest.fixture
async def insert_parsed_service():
    async with async_session() as session:
        service = M.ParsedService(name="example-service")
        session.add(service)
        await session.commit()
    yield
    await update_db()


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
