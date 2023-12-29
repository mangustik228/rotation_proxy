from datetime import datetime

from freezegun import freeze_time
from sqlalchemy import text

import app.repo as R
from app.db_postgres import async_session


@freeze_time("2023-12-25T12:00:00")
async def test_get_last_5(insert_proxies_10_proxies, insert_parsed_services):
    q = """
        INSERT INTO 
        error(reason, created_at, proxy_id, parsed_service_id, sleep_time) 
        VALUES
        ('cloudflare', '2023-12-25T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-25T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-25T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-24T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-23T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-22T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-20T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-20T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-20T10:00:00', 1, 1, 300),
        ('cloudflare', '2023-12-25T10:00:00', 1, 2, 300),
        ('cloudflare', '2023-12-20T10:00:00', 1, 1, 300)"""
    async with async_session() as session:
        await session.execute(text(q))
        await session.commit()
    result = await R.Error.get_last_hours(1, 1, ignore_hours=24)
    assert len(result) == 3
    result = await R.Error.get_last_hours(1, 1, ignore_hours=48)
    assert len(result) == 4
    result = await R.Error.get_last_hours(1, 1, ignore_hours=500)
    assert len(result) == 10
    for item in result:
        assert isinstance(item.date, datetime)
        assert isinstance(item.sleep, int)
    result = await R.Error.get_last_hours(1, 1, ignore_hours=1)
    assert len(result) == 0
    result = await R.Error.get_last_hours(1, 2, ignore_hours=25)
    assert len(result) == 1
    result = await R.Error.get_last_hours(2, 1, ignore_hours=25)
    assert len(result) == 0
