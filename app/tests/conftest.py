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
from sqlalchemy import insert

import app.models as M
from app.db_postgres import engine, async_session
from app.main import app as fastapi_app

from alembic import command
from alembic.config import Config


@pytest.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def insert_proxies():
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


# class _NameSpace:
#     file_path = 'tests/src/test_ids'
#     debug = True


# @pytest.fixture(autouse=True)
# def mock_get_namespace(mocker):
#     mocker.patch('app.config.arg_parser.get_namespace',
#                  return_value=_NameSpace())
