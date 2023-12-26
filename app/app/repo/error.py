from .base_repo import BaseRepo
import app.models as M
from app.db_postgres import async_session
from sqlalchemy import select, desc
from datetime import datetime, timedelta
from collections import namedtuple


block = namedtuple("Block", ["date", "sleep"])


class Error(BaseRepo):
    model = M.Error

    @classmethod
    async def get_last_hours(cls, proxy_id: int,  parsed_service_id: int, ignore_hours: int) -> list[block]:
        time = datetime.utcnow() - timedelta(hours=ignore_hours)
        async with async_session() as session:
            stmt = select(cls.model.created_at, cls.model.sleep_time)\
                .where(cls.model.proxy_id == proxy_id)\
                .where(cls.model.parsed_service_id == parsed_service_id)\
                .where(cls.model.created_at > time)\
                .order_by(desc(cls.model.created_at))
            items = await session.execute(stmt)
            data = []
            for item in items:
                data.append(block(date=item.created_at, sleep=item.sleep_time))
            return data

    @classmethod
    async def get_by_proxy_id(cls, proxy_id: int):
        async with async_session() as session:
            stmt = select(cls.model)\
                .where(cls.model.proxy_id == proxy_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_by_service_id(cls, parsed_service_id: int):
        async with async_session() as session:
            stmt = select(cls.model)\
                .where(cls.model.parsed_service_id == parsed_service_id)
            result = await session.execute(stmt)
            return result.scalars().all()
