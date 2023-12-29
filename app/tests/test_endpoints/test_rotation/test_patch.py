import pytest
from httpx import AsyncClient
from tests.utils import ProxyBuilderPatch

import app.repo as R


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


async def test_change_proxy_not_available(insert_5_proxy_to_change, client: AsyncClient):
    builder = ProxyBuilderPatch()
    builder.set_proxy_id(1)
    for _ in range(4):
        data = builder.build()
        response = await client.patch("/proxies/rotations", json=data)
        new_proxy_id = response.json()["id"]
        builder.set_proxy_id(new_proxy_id)

    await R.ProxyBlocked.get_all() == 4
    await R.ProxyBusy.get_all() == 4


async def test_change_proxy_expired_from_another_service(insert_5_proxy_to_change, client: AsyncClient):
    builder = ProxyBuilderPatch()
    for i in range(1, 6):
        await R.ProxyBlocked.add(i, "example-service")
    await R.ParsedService.add_one(name="ozon")

    data = builder.build()
    response = await client.patch("/proxies/rotations", json=data)
    assert response.status_code == 404

    builder.set_parsed_service("ozon")
    data = builder.build()

    response = await client.patch("/proxies/rotations", json=data)
    assert response.status_code == 200
    blocks = await R.ProxyBlocked.get_all_by_service("ozon")
    assert len(blocks) == 1
