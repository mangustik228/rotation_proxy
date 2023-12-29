import asyncio

import pytest
from httpx import AsyncClient

from app.config import settings
from app.main import app as fastapi_app

# Из документации pytest


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(
            app=fastapi_app,
            base_url="http://test",
            headers={"X-API-Key": settings.APIKEY}
    ) as ac:
        yield ac
