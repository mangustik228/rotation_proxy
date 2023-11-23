from httpx import AsyncClient
import os

import pytest
from tests.utils import ProxyBuilder


async def test_get_proxies_insert_10(client: AsyncClient, insert_proxies):
    result = await client.get('/proxies')
    assert result.status_code == 200
    assert len(result.json()) == 9


async def test_get_proxies_empty(client: AsyncClient):
    result = await client.get("/proxies")
    assert result.status_code == 200
    assert len(result.json()) == 0


async def test_post_proxies(client: AsyncClient):
    proxy_builder = ProxyBuilder()
    data = proxy_builder.build_list()
    response = await client.post("/proxies", json=data)
    assert response.status_code == 201
    assert response.json() == {"status": "ok"}
    response = await client.post("/proxies", json=data)
    assert response.status_code == 409


async def test_post_proxies_with_minimum_settings(client: AsyncClient):
    proxy_builder = ProxyBuilder()
    proxy_builder.delete_field("location_id")
    proxy_builder.delete_field("type_id")
    data = proxy_builder.build_list()
    response = await client.post("/proxies", json=data)
    assert response.status_code == 201
    assert response.json() == {"status": "ok"}
