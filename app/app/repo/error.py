from collections import namedtuple
from datetime import datetime, timedelta

from sqlalchemy import desc, func, select

import app.models as M
from app.db_postgres import async_session

from .base_repo import BaseRepo

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

    @classmethod
    async def get_count_by_service_id_last_time(cls, parsed_service_id: int, hours: int):
        time = datetime.utcnow() - timedelta(hours=hours)
        async with async_session() as session:
            stmt = select(func.count())\
                .select_from(cls.model)\
                .where(cls.model.created_at > time)\
                .where(cls.model.parsed_service_id == parsed_service_id)
            result = await session.execute(stmt)
            return result.scalar_one()

    @classmethod
    async def get_count_errors_by_service(cls, parsed_service_id):
        async with async_session() as session:
            stmt = select(func.count())\
                .select_from(cls.model)\
                .where(cls.model.parsed_service_id == parsed_service_id)
            result = await session.execute(stmt)
            return result.scalar_one()

    @classmethod
    async def get_time_last_error(cls, parsed_service_id):
        async with async_session() as session:
            stmt = select(func.min(cls.model.created_at))\
                .select_from(cls.model)\
                .where(cls.model.parsed_service_id == parsed_service_id)
            result = await session.execute(stmt)
            return result.scalar_one()

    @classmethod
    async def get_group_errors_by_service(cls, service_id: int):
        async with async_session() as session:
            stmt = select(cls.model.reason, func.count())\
                .group_by(cls.model.reason)\
                .where(cls.model.parsed_service_id == service_id)
            result = await session.execute(stmt)
            return result.mappings().all()

    @classmethod
    async def group_by_reasons(cls):
        async with async_session() as session:
            stmt = select(
                cls.model.reason,
                M.ParsedService.name,
                func.count(cls.model.reason))\
                .group_by(cls.model.reason, M.ParsedService.name).join(M.ParsedService)
            result = await session.execute(stmt)
            return result.mappings().all()

    @classmethod
    async def get_stats_by_services(cls):
        '''
            SELECT s.name, e.reason, p.id, count(*)
            FROM error e 
            JOIN proxy p ON p.id = e.proxy_id
            JOIN service s ON p.service_id = s.id
            GROUP BY s.name, p.id, e.reason
        '''
        async with async_session() as session:
            stmt = select(
                M.Service.name,
                M.Error.reason,
                M.Proxy.id,
                func.count().label("error_count")
            )\
                .select_from(M.Error)\
                .join(M.Proxy, M.Proxy.id == M.Error.proxy_id)\
                .join(M.Service, M.Service.id == M.Proxy.service_id)\
                .group_by(M.Service.name, M.Error.reason, M.Proxy.id)
            result = await session.execute(stmt)
            return result.mappings().all()
