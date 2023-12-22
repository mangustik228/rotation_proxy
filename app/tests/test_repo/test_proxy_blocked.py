import pytest
import app.repo as R
import asyncio
from app.db_redis import REDIS


async def test_get_empty():
    result = await R.ProxyBlocked.get_all()
    print(result)
    assert len(result) == 0


async def test_add():
    await R.ProxyBlocked.add(1, "example", 2)
    result = await REDIS.get("blocked_example_1")
    assert result == b'1'


async def test_get_all(insert_blocked):
    result = await R.ProxyBlocked.get_all()
    print(result)
    assert isinstance(result[0], str)


@pytest.mark.parametrize("service,expected", [
    ("example", 0),
    ("test-example", 4)])
async def test_get_all_by_service_empty(insert_blocked, service, expected):
    result = await R.ProxyBlocked.get_all_by_service(service)
    assert len(result) == expected


async def test_free(insert_blocked):
    await R.ProxyBlocked.free(1, "test-example")
    result = await REDIS.get("blocked_test-example_1")
    assert result == None


@pytest.mark.parametrize("service,id,expected", [
    ("example", 1, False),
    ("test-example", 1, True),
    ("test-example", 11, False),
])
async def test_is_blocked(insert_blocked, service, id, expected):
    result = await R.ProxyBlocked.is_blocked_by_service(id, service)
    assert result == expected


@pytest.mark.parametrize("id,expected", [
    (1, ["test-example", "test-example-2"]),
    (6, []),
    ("1", ["test-example", "test-example-2"])
])
async def test_where_is_blocked_true(insert_blocked, id, expected):
    result = await R.ProxyBlocked.where_id_blocked(id)
    assert result == expected
