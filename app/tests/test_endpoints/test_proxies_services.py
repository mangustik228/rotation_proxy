from httpx import AsyncClient
import pytest
from tests.utils import ProxyServiceBuilder


async def test_get_services(client: AsyncClient):
    result = await client.get("/services")
    assert result.status_code == 200
    assert len(result.json()) == 1


async def test_post_services(client: AsyncClient, clear_db):
    builder = ProxyServiceBuilder()
    builder.set_name("hello world")
    service = builder.build()
    result = await client.post("/services", json=service)
    assert result.status_code == 201
    assert result.json()["service"]["name"] == "hello world"
    assert result.json()["service"]["id"] == 2


async def test_post_services_dublicates(client: AsyncClient, clear_db):
    service = ProxyServiceBuilder().build()
    for _ in range(2):
        result = await client.post("/services", json=service)
    assert result.status_code == 409


async def test_put_services(client: AsyncClient, clear_db):
    builder = ProxyServiceBuilder()
    builder.set_name("world")
    service = builder.build()
    response = await client.put("/services/1", json=service)
    assert response.status_code == 201


async def test_get_one(client: AsyncClient):
    response = await client.get("/services/1")
    assert response.status_code == 200


async def test_get_one_empty(client: AsyncClient):
    response = await client.get("/services/2")
    assert response.status_code == 404
