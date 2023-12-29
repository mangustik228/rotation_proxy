import asyncio

import pytest

import app.repo as R
from app.db_redis import REDIS


async def test_get_empty(redis_clear):
    result = await R.ProxyBlocked.get_all()
    assert len(result) == 0


async def test_add():
    await R.ProxyBlocked.add(1, "example", 2)
    result = await REDIS.get("blocked_example_1")
    assert result == b'1'


async def test_get_all(redis_insert_blocked_10):
    result = await R.ProxyBlocked.get_all()
    assert isinstance(result[0], str)
    assert len(result) == 8


@pytest.mark.parametrize("service,expected", [
    ("service", 0),
    ("test-service", 4)])
async def test_get_all_by_service_empty(redis_insert_blocked_10, service, expected):
    result = await R.ProxyBlocked.get_all_by_service(service)
    assert len(result) == expected


async def test_free(redis_insert_blocked_10):
    await R.ProxyBlocked.free(1, "test-service")
    result = await REDIS.get("blocked_test-service_1")
    assert result == None


@pytest.mark.parametrize("service,id,expected", [
    ("service", 1, True),
    ("test-service", 1, False),
    ("test-service", 11, True),
])
async def test_is_blocked(redis_clear, redis_insert_blocked_10, service, id, expected):
    result = await R.ProxyBlocked.is_free(id, service)
    assert result == expected


@pytest.mark.parametrize("id,expected", [
    (1, ["test-service", "test-service-2"]),
    (6, []),
    ("1", ["test-service", "test-service-2"])
])
async def test_where_is_blocked_true(redis_insert_blocked_10, id, expected):
    data = await R.ProxyBlocked.where_id_blocked(id)
    for datum in data:
        assert datum in expected


@pytest.mark.parametrize("id,service,expected", [
    (1, "test-service", 7),
    (1, "testik", 8),
])
async def test_delete(redis_insert_blocked_10, id, service, expected):
    await R.ProxyBlocked.free(id, service)
    result = await REDIS.get(f"blocked_{service}_{id}")
    assert result == None, service
    result = await REDIS.keys()
    assert len(result) == expected
