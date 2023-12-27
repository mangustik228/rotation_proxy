from httpx import AsyncClient
from tests.utils import ProxyBuilderPatch
import app.repo as R


async def test_integration(insert_5_proxy_to_change, client: AsyncClient):
    # Получаем 2 прокси.
    params = {"parsed_service_id": 1, "count": 2}
    response = await client.get("/proxies/rotations", params=params)
    proxies = response.json()["data"]
    result = await R.ProxyBusy.get_all()
    assert len(result) == 2

    builder = ProxyBuilderPatch()
    for proxy in proxies:
        proxy_id = proxy["id"]
        builder.set_proxy_id(proxy_id)
        data = builder.build()
        response = await client.patch("/proxies/rotations", json=data)
        assert response.status_code == 200
        new_proxy = response.json()
        new_proxy_id = new_proxy["id"]

    result = await R.ProxyBusy.get_all()
    assert len(result) == 2

    result = await R.ProxyBlocked.get_all()
    assert len(result) == 2

    builder.set_proxy_id(new_proxy_id)
    data = builder.build()
    response = await client.patch("/proxies/rotations", json=data)
    result = await R.ProxyBlocked.get_all()
    assert len(result) == 3
    new_proxy_id = response.json()["id"]

    result = await R.ProxyBusy.get_all()
    assert len(result) == 2

    builder.set_proxy_id(new_proxy_id)
    data = builder.build()
    response = await client.patch("/proxies/rotations", json=data)
    assert response.status_code == 404

    busy = await R.ProxyBusy.get_all()
    assert len(busy) == 1

    blocks = await R.ProxyBlocked.get_all()
    assert len(blocks) == 4
