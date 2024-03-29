
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import settings
from app.main import app as fastapi_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(fastapi_app, headers={"X-API-KEY": settings.APIKEY})


@pytest.fixture()
async def async_client() -> AsyncClient:
    async with AsyncClient(
            app=fastapi_app,
            base_url="http://test",
            headers={"X-API-Key": settings.APIKEY}
    ) as ac:
        yield ac
