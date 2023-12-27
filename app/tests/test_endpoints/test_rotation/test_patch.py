from httpx import AsyncClient
import pytest
import app.repo as R
from tests.utils import ChangeProxyBuilder


async def test_change_proxy_base(set_5_proxy_to_change, client: AsyncClient):
    builder = ChangeProxyBuilder()
    builder.set_proxy_id(1)
    data = builder.build()
    response = await client.patch("/proxies/rotations", json=data)
    assert response.status_code == 200


async def test_change_proxy_error_db(set_5_proxy_to_change, client: AsyncClient):
    builder = ChangeProxyBuilder()
    builder.set_proxy_id(2)
    data = builder.build()
    await client.patch("/proxies/rotations", json=data)
    result = await R.Error.count_items()
    assert result == 1


@pytest.mark.skip
async def test_change_proxy_error_redis(set_5_proxy_to_change, client: AsyncClient):
    builder = ChangeProxyBuilder()
    builder.set_proxy_id(2)
    data = builder.build()
    await client.patch("/proxies/rotations", json=data)
    # TODO


@pytest.mark.skip
async def test_change_proxy_not_available(set_5_proxy_to_change, client: AsyncClient):
    builder = ChangeProxyBuilder()
    for i in range(1, 6):
        builder.set_proxy_id(i)
        data = builder.build()
        response = await client.patch("/proxies/rotations", json=data)
        print(response.json())
        assert response.status_code == 200
    response = await client.patch("/proxies/rotations/1")
