from httpx import AsyncClient
import pytest
import app.repo as R
from tests.utils import ProxyBuilderPatch


async def test_change_proxy_base(insert_5_proxy_to_change, client: AsyncClient):
    builder = ProxyBuilderPatch()
    builder.set_proxy_id(1)
    data = builder.build()
    response = await client.patch("/proxies/rotations", json=data)
    assert response.status_code == 200


async def test_change_proxy_error_db(insert_5_proxy_to_change, client: AsyncClient):
    builder = ProxyBuilderPatch()
    builder.set_proxy_id(2)
    data = builder.build()
    await client.patch("/proxies/rotations", json=data)
    result = await R.Error.count_items()
    assert result == 1


@pytest.mark.skip
async def test_change_proxy_error_redis(insert_5_proxy_to_change, client: AsyncClient):
    builder = ProxyBuilderPatch()
    builder.set_proxy_id(2)
    data = builder.build()
    await client.patch("/proxies/rotations", json=data)


@pytest.mark.skip
async def test_change_proxy_not_available(insert_5_proxy_to_change, client: AsyncClient):
    builder = ProxyBuilderPatch()
    builder.set_proxy_id(i)
    data = builder.build()
    response = await client.patch("/proxies/rotations", json=data)
    response = await client.patch("/proxies/rotations/1")
