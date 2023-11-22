from httpx import AsyncClient
import os

import pytest
from tests.utils import ProxyBuilder


async def test_get_proxies_insert_10(async_client: AsyncClient, insert_proxies):
    result = await async_client.get('/proxies')
    assert result.status_code == 200
    assert len(result.json()) == 9


async def test_get_proxies_empty(async_client: AsyncClient):
    result = await async_client.get("/proxies")
    assert result.status_code == 200
    assert len(result.json()) == 0


async def test_post_proxies(async_client: AsyncClient):
    proxy_builder = ProxyBuilder()
    data = proxy_builder.build()
    response = await async_client.post("/proxies", json=data)
    assert response.status_code == 201
    assert response.json() == {"status": "ok"}

    response = await async_client.post("/proxies", json=data)
    assert response.status_code == 409


async def test_post_proxies_with_minimum_settings(async_client: AsyncClient):
    proxy_builder = ProxyBuilder()
    proxy_builder.delete_field("location")
    proxy_builder.delete_field("type_id")
    data = proxy_builder.build()
    print(data)
    response = await async_client.post("/proxies", json=data)
    assert response.status_code == 201
    assert response.json() == {"status": "ok"}
