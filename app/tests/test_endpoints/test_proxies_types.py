from httpx import AsyncClient
from tests.utils import ProxyTypesBuilder


async def test_get_list(client: AsyncClient):
    response = await client.get("/types")
    assert response.status_code == 200
    data = response.json()
    assert len(data["types"]) == 1


async def test_get_one(client: AsyncClient):
    response = await client.get("/types/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "IPv4"


async def test_get_one_empty(client: AsyncClient):
    response = await client.get("/types/2")
    assert response.status_code == 404


async def test_post_proxy(client: AsyncClient, clear_db):
    proxy_type = ProxyTypesBuilder().build()
    response = await client.post("/types", json=proxy_type)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["type"]["name"] == "IPv6"


async def test_post_proxy_dublicates(client: AsyncClient, clear_db):
    proxy_type = ProxyTypesBuilder().build()
    for i in range(2):
        response = await client.post("/types", json=proxy_type)
    assert response.status_code == 409


async def test_put_proxy(client: AsyncClient, clear_db):
    proxy_type = ProxyTypesBuilder().build()
    response = await client.put("/types/1", json=proxy_type)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["type"]["name"] == "IPv6"


async def test_put_proxy_empty(client: AsyncClient, clear_db):
    proxy_type = ProxyTypesBuilder().build()
    response = await client.put("/types/2", json=proxy_type)
    assert response.status_code == 404


async def test_put_get_proxy(client: AsyncClient, clear_db):
    builder = ProxyTypesBuilder()
    proxy_type_name = "shared"
    builder.set_name(proxy_type_name)
    data = builder.build()
    response = await client.put("/types/1", json=data)
    assert response.status_code == 201

    response = await client.get("/types/1")
    data = response.json()
    assert data["name"] == proxy_type_name
