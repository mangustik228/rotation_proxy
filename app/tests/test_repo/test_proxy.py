from app.db_postgres import async_session
import app.repo as R
from tests.utils import ProxyBuilder
from sqlalchemy import text


async def get_count_items_in_db() -> int:
    q = "select count(*) from proxy"
    async with async_session() as session:
        result = await session.execute(text(q))
        return result.scalar_one()


async def test_count():
    result = await R.Proxy.count_items()
    assert result == 0


async def test_count_full(insert_proxies_10_proxies):
    result = await R.Proxy.count_items()
    assert result == 10


async def test_add_one(clear_db):
    builder = ProxyBuilder()
    builder.set_server("100.100.100.100")
    data = builder.build()
    before = await R.Proxy.count_items()
    await R.Proxy.add_one(**data)
    after = await R.Proxy.count_items()
    assert before + 1 == after
