import json
import os
from datetime import datetime
import asyncio
from httpx import AsyncClient
import pytest
from sqlalchemy import insert

from app.main import app as fastapi_app
from app.db_postgres import engine, async_session
import app.models as M

os.environ["MODE"] = "TEST"


@pytest.fixture()
async def async_client() -> AsyncClient:
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
    async with engine.begin() as conn:
        await conn.run_sync(M.Base.metadata.drop_all)
        await conn.run_sync(M.Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    await update_db()


# Из документации pytest
@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# class _NameSpace:
#     file_path = 'tests/src/test_ids'
#     debug = True


# @pytest.fixture(autouse=True)
# def mock_get_namespace(mocker):
#     mocker.patch('app.config.arg_parser.get_namespace',
#                  return_value=_NameSpace())
