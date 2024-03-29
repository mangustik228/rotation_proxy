from sqlalchemy import text

import app.repo as R
from app.db_postgres import async_session
from app.db_redis import REDIS
from app.services import FacadeRotationAvailable, FacadeRotationPatch


async def test_facade_rotation_available(redis_clear, sql_insert_10_proxies):
    facade = FacadeRotationAvailable("example", 4, None, 1, 1, 300)
    await facade.get_available_from_sql()
    # 1 из прокси просроченный
    assert len(facade.proxies_models) == 9
    await facade.prepare_proxies()
    assert len(facade.result["data"]) == 4


async def test_facade_rotation_available_blocked(redis_clear, sql_insert_10_proxies):
    q = "INSERT INTO parsed_service(name) VALUES('test-service')"
    async with async_session() as session:
        await session.execute(text(q))
    for i in range(1, 8):
        await REDIS.set(f"blocked_test-service_{i}", 1)
    facade = FacadeRotationAvailable("test-service", 5, None, 1, 1, 300)
    await facade.get_available_from_sql()
    await facade.prepare_proxies()
    assert facade.result["status"] == "not full"
    # 8, 9, 10
    assert len(facade.result["data"]) == 3


async def test_facade_rotation_available_buzy(redis_clear, sql_insert_10_proxies):
    for i in range(5, 15):
        await REDIS.set(f"busy_{i}", 1)
    facade = FacadeRotationAvailable("example", 10, None, 1, 1, 5)
    await facade.get_available_from_sql()
    await facade.prepare_proxies()
    assert facade.result["status"] == "not full"
    assert len(facade.result["data"]) == 3
    for item in facade.result["data"]:
        assert item.id in (2, 3, 4)
