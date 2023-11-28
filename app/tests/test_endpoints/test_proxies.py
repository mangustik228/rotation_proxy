import asyncio
import json
from httpx import AsyncClient
import os

import pytest
from tests.utils import ProxyBuilder


async def test_get_proxies(client: AsyncClient, insert_proxies_10_proxies):
    response = await client.get("/proxies")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 10
    assert data["total_active_count"] == 9
    assert len(data["proxies"]) == 10


async def test_post_proxy(client: AsyncClient, clear_db):
    data = ProxyBuilder().build()
    response = await client.post("/proxies", json=data)
    assert response.status_code == 201


async def test_post_proxy_dublicated(client: AsyncClient, clear_db):
    data = ProxyBuilder().build()
    for _ in range(2):
        response = await client.post("/proxies", json=data)
    assert response.status_code == 409


async def test_post_proxy_bulk(client: AsyncClient, clear_db):
    builder = ProxyBuilder()
    data = []
    for i in range(1, 15):
        builder.set_server(f"255.255.{i}.1")

        data.append(builder.build())
    response = await client.post("/proxies/bulk", json=data)
    assert response.status_code == 201
    assert response.json()["count_added"] == 14
    assert response.json()["status"] == "created"


async def test_put_proxy(client: AsyncClient, insert_proxies_10_proxies, clear_db):
    with open("./tests/src/proxies.json") as fp:
        data: list[dict] = json.load(fp)
    proxy = data[0]
    proxy["port"] = 9999
    response = await client.put("/proxies/1", json=proxy)
    assert response.status_code == 201
    assert response.json()["status"] == "updated"


async def test_delete_proxy(client: AsyncClient, insert_proxies_10_proxies, clear_db):
    response = await client.delete("/proxies/1")
    # assert response.status_code == 204
    await asyncio.sleep(0.5)
    response = await client.delete("/proxies/1")
    assert response.status_code == 404


async def test_putch_proxy(client: AsyncClient, insert_proxies_10_proxies, clear_db):
    data = {"server": "192.0.123.3"}
    response = await client.patch("/proxies/1", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "updated"


async def test_putch_proxy_error(client: AsyncClient, insert_proxies_10_proxies, clear_db):
    builder = ProxyBuilder()
    builder.set_expire("2023-11-30")
    data = builder.build()
    for i in range(1, 3):
        response = await client.patch(f"/proxies/{i}", json=data)
    assert response.status_code == 409

# async def
#
# test_get_proxies_empty(client: AsyncClient):
#     result = await client.get("/proxies")
#     assert result.status_code == 200
#     assert len(result.json()) == 0


# async def test_post_proxies(client: AsyncClient):
#     proxy_builder = ProxyBuilder()
#     data = proxy_builder.build_list()
#     response = await client.post("/proxies", json=data)
#     assert response.status_code == 201
#     assert response.json() == {"status": "ok"}
#     response = await client.post("/proxies", json=data)
#     assert response.status_code == 409


# async def test_post_proxies_with_minimum_settings(client: AsyncClient):
#     proxy_builder = ProxyBuilder()
#     proxy_builder.delete_field("location_id")
#     proxy_builder.delete_field("type_id")
#     data = proxy_builder.build_list()
#     response = await client.post("/proxies", json=data)
#     assert response.status_code == 201
#     assert response.json() == {"status": "ok"}
