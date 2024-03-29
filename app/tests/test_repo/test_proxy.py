from sqlalchemy import text
from tests.utils import ProxyBuilder

import app.repo as R
from app.db_postgres import async_session


async def get_count_items_in_db() -> int:
    q = "select count(*) from proxy"
    async with async_session() as session:
        result = await session.execute(text(q))
        return result.scalar_one()


async def test_count():
    result = await R.Proxy.count_items()
    assert result == 0


async def test_count_full(sql_insert_10_proxies):
    result = await R.Proxy.count_items()
    assert result == 10


async def test_add_one(sql_clear):
    builder = ProxyBuilder()
    builder.set_server("100.100.100.100")
    data = builder.build()
    before = await R.Proxy.count_items()
    await R.Proxy.add_one(**data)
    after = await R.Proxy.count_items()
    assert before + 1 == after
