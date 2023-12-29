import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from tests.utils import ProxyBuilder

import app.repo as R


def test_get_proxies(client: TestClient, sql_insert_10_proxies):
    response = client.get("/proxies")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 10
    assert data["total_active_count"] == 9
    assert len(data["proxies"]) == 10


def test_post_proxy(client: TestClient, sql_clear):
    data = ProxyBuilder().build_to_endpoint()
    response = client.post("/proxies", json=data)
    assert response.status_code == 201


def test_post_proxy_dublicated(client: TestClient, sql_clear):
    data = ProxyBuilder().build_to_endpoint()
    for _ in range(2):
        response = client.post("/proxies", json=data)
    assert response.status_code == 409


async def test_delete_proxy(async_client: AsyncClient, sql_insert_10_proxies, sql_clear):
    response = await async_client.delete("/proxies/1")
    # assert response.status_code == 204
    await asyncio.sleep(0.5)
    response = await async_client.delete("/proxies/1")
    assert response.status_code == 404


def test_post_proxy_bulk(sql_clear, client: TestClient):
    builder = ProxyBuilder()
    data = []
    for i in range(1, 15):
        builder.set_server(f"255.255.{i}.1")
        data.append(builder.build_to_endpoint())
    response = client.post("/proxies/bulk", json=data)
    assert response.status_code == 201
    assert response.json()["count_added"] == 14
    assert response.json()["status"] == "created"


async def test_put_proxy(client: TestClient, sql_insert_10_proxies):
    with open("./tests/src/proxies.json") as fp:
        data: list[dict] = json.load(fp)
    proxy = data[0]
    proxy["port"] = 9999
    response = client.put("/proxies/1", json=proxy)
    assert response.status_code == 201
    assert response.json()["status"] == "updated"


def test_putch_proxy(client: TestClient, sql_insert_10_proxies):
    data = {"server": "192.0.123.3"}
    response = client.patch("/proxies/1", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "updated"


def test_putch_proxy_error(client: TestClient, sql_insert_10_proxies):
    builder = ProxyBuilder()
    builder.set_expire(datetime(year=2023, month=11, day=30))
    data = builder.build_to_endpoint()
    for i in range(1, 3):
        response = client.patch(f"/proxies/{i}", json=data)
    assert response.status_code == 409
