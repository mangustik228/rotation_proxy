import pytest
from httpx import AsyncClient

import app.repo as R
from app.db_redis import REDIS


async def test_get_busies(clear_redis, client: AsyncClient):
    for i in range(1, 6):
        await R.ProxyBusy.add(i)
    response = await client.get("/proxies/busies")
    assert len(response.json()) == 5


async def test_get_blocked(clear_redis, client: AsyncClient):
    for i in range(1, 6):
        await R.ProxyBlocked.add(i, "world")
    response = await client.get("/proxies/blocks")
    assert len(response.json()) == 5
