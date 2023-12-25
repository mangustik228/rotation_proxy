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


async def test_get_errors_by_proxy_id(
        insert_proxies_10_proxies,
        insert_3_errors,
        client: AsyncClient):
    response = await client.get("/errors/proxy/1")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert result["count"] == 3
    assert result["proxy"]["id"] == 1


async def test_get_errors_by_proxy_id_exception(client: AsyncClient):
    response = await client.get("/errors/proxy/1")
    assert response.status_code == 404


async def test_get_errors_by_parsed_service(
    insert_proxies_10_proxies,
    insert_3_errors,
    client: AsyncClient
):
    response = await client.get("/errors/parsed_service/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 3
    assert data["parsed_service"]["id"] == 1
    assert data["parsed_service"]["name"] == "example-service"
