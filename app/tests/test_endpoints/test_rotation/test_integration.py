from httpx import AsyncClient
from tests.utils import ProxyBuilderPatch

import app.repo as R


async def test_integration(insert_5_proxy_to_change, async_client: AsyncClient, ):
    # Получаем 2 прокси.
    params = {"parsed_service_id": 1, "count": 2}
    response = await async_client.get("/proxies/rotations", params=params)
    proxies = response.json()["data"]
    result = await R.ProxyBusy.get_all()
    assert len(result) == 2
    builder = ProxyBuilderPatch()

    # busy - 2 , block - 1
    proxy_id = proxies[0]["id"]
    builder.set_proxy_id(proxy_id)
    data = builder.build()
    response = await async_client.patch("/proxies/rotations", json=data)
    assert response.status_code == 200

    # busy -2 block -2
    new_proxy_id = response.json()["id"]
    builder.set_proxy_id(new_proxy_id)
    data = builder.build()
    response = await async_client.patch("/proxies/rotations", json=data)
    assert response.status_code == 200

    busies = await R.ProxyBusy.get_all()
    blocks = await R.ProxyBlocked.get_all()
    assert len(busies) == len(blocks)

    # busy - 2, block - 3
    new_proxy_id = response.json()["id"]
    builder.set_proxy_id(new_proxy_id)
    data = builder.build()
    response = await async_client.patch("/proxies/rotations", json=data)
    result = await R.ProxyBlocked.get_all()
    assert len(result) == 3
    new_proxy_id = response.json()["id"]

    assert len(await R.ProxyBusy.get_all()) == 2

    builder.set_proxy_id(new_proxy_id)
    data = builder.build()
    response = await async_client.patch("/proxies/rotations", json=data)
    assert response.status_code == 404

    assert len(await R.ProxyBusy.get_all()) == 1
    assert len(await R.ProxyBlocked.get_all()) == 4

    new_service = await R.ParsedService.add_one(name="ozon")
    params = {"parsed_service_id": new_service.id, "count": 5}

    response = await async_client.get("/proxies/rotations", params=params)
    assert response.status_code == 200
    assert response.json()["status"] == "not full"
    assert len(response.json()["data"]) == 4

    response = await async_client.get("/errors/parsed_service/1")
    data = response.json()
    assert data["count"] == 4
    assert data["status"] == "success"
    assert data["parsed_service"]["id"] == 1
    assert data["parsed_service"]["name"] == "example-service"
    assert len(data["errors"]) == 4
