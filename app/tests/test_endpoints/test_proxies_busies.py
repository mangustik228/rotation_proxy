import pytest
from httpx import AsyncClient

import app.repo as R
from app.db_redis import REDIS


@pytest.mark.skip
async def test_get_busies(client: AsyncClient):
    busies = await R.ProxyBusy.get_all()
    result = []
    for key, value in busies:
        item = {}
        item["id"] = key.split("_")[-1]
        item["expire"] = value
        result.append(item)
    return result
    # TODO
