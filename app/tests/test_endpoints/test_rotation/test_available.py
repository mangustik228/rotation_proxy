from datetime import datetime
from httpx import AsyncClient
import pytest
from app.db_postgres import async_session
from app.db_redis import REDIS
import app.repo as R
from tests.utils import ProxyBuilder


async def test_availables_proxies_simple(
        insert_proxies_10_proxies,
        insert_parsed_services,
        clear_redis,
        client: AsyncClient):
    params = {"parsed_service_id": 1}
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 200
    assert response.json()["status"] == "full"
    # assert response.status_code == 200


async def test_availables_proxies_not_full(
        insert_proxies_10_proxies,
        insert_parsed_services,
        clear_redis,
        client: AsyncClient):
    params = {"parsed_service_id": 1, "location_id": 2}
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 404


async def test_availables_proxies_error(insert_proxies_10_proxies, client: AsyncClient):
    params = {"parsed_service_id": 5}
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 409
    assert response.json()[
        "detail"] == "Parsed_service with id: 5 doesn't exist"


async def test_availables_proxies_count(
        insert_proxies_10_proxies,
        insert_parsed_services,
        clear_redis,
        client: AsyncClient):
    params = {"parsed_service_id": 1, "count": 15}
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 200
    assert response.json()["status"] == "not full"
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"]) == 9


async def test_availables_proxies_types(
        insert_proxies_10_proxies,
        insert_parsed_services,
        client: AsyncClient,
        clear_redis):
    await R.ProxyType.add_one(name="IPv6")
    builder = ProxyBuilder()
    builder.set_server("100.100.100.100")
    builder.set_type_id(2)
    data = builder.build()
    await R.Proxy.add_one(**data)

    params = {"parsed_service_id": 1, "type_id": 2}
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 200
    assert response.json()["status"] == "not full"
    assert response.json()["data"][0]["server"] == "100.100.100.100"
    assert len(response.json()["data"]) == 1


async def test_availables_proxies_expire(
        insert_proxies_10_proxies,
        insert_parsed_services,
        client: AsyncClient,
        clear_redis):
    builder = ProxyBuilder()
    builder.set_server("100.100.100.100")
    builder.set_expire(datetime(year=2025, month=12, day=30))
    data = builder.build_to_repo()
    await R.Proxy.add_one(**data)

    params = {"parsed_service_id": 1, "expire_proxy": "2025-12-29T12:00:00"}
    response = await client.get("/proxies/rotations", params=params)

    assert response.status_code == 200
    assert response.json()["status"] == "not full"
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["server"] == "100.100.100.100"


async def test_redis_writer(
        insert_proxies_10_proxies,
        insert_parsed_services,
        client: AsyncClient,
        clear_redis):
    params = {"parsed_service_id": 1, "count": 3}
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 200
    keys: list[bytes] = await REDIS.keys("*")
    keys = [k.decode() for k in keys if "busy_" in k.decode()]
    assert len(keys) == 3
