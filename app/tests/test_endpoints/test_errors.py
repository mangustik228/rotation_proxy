from httpx import AsyncClient
from tests.utils import ErrorBuilder


async def test_post_errors(insert_proxies_10_proxies, insert_parsed_service, client: AsyncClient):
    data = ErrorBuilder().build()
    response = await client.post("/errors", json=data)
    assert response.status_code == 201, response.json()
    result = response.json()
    assert result["status"] == "created"
    assert result["error_id"] == 1


async def test_post_errors_wrong_status(client: AsyncClient):
    builder = ErrorBuilder()
    builder.set_proxy_id(100)
    data = builder.build()
    response = await client.post("/errors", json=data)
    assert response.status_code == 404


async def test_get_errors_by_id(client: AsyncClient):
    ...
