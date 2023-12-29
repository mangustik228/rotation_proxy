from datetime import datetime

from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload

import app.models as M
from app.db_postgres import async_session
from app.db_redis import redis_cache

from .base_repo import BaseRepo, check_alchemy_problem


class Proxy(BaseRepo):
    model = M.Proxy

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            stmt = \
                select(M.Proxy)\
                .options(
                    selectinload(M.Proxy.location),
                    selectinload(M.Proxy.proxy_type),
                    selectinload(M.Proxy.service))
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id: int):
        async with async_session() as session:
            stmt = select(M.Proxy)\
                .where(M.Proxy.id == id)\
                .options(
                    selectinload(M.Proxy.location),
                    selectinload(M.Proxy.proxy_type),
                    selectinload(M.Proxy.service))
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_total_count(cls) -> int:
        async with async_session() as session:
            stmt = select(func.count()).select_from(M.Proxy)
            result = await session.execute(stmt)
            return result.scalar()

    @classmethod
    async def get_active_count(cls) -> int:
        async with async_session() as session:
            stmt = select(func.count())\
                .select_from(M.Proxy)\
                .where(M.Proxy.expire > datetime.now())
            result = await session.execute(stmt)
            return result.scalar()

    @classmethod
    @check_alchemy_problem
    async def update_fields(cls, id: int, **data):
        async with async_session() as session:
            stmt = update(M.Proxy).where(M.Proxy.id == id).values(
                **data).returning(M.Proxy)
            result = await session.execute(stmt)
            data = result.scalar()
            await session.commit()
            return data

    @classmethod
    @redis_cache
    async def get_available(cls, expire: datetime, location_id: int, type_id: int):
        async with async_session() as session:
            stmt = select(
                M.Proxy.id,
                M.Proxy.server,
                M.Proxy.port,
                M.Proxy.username,
                M.Proxy.password,
            ).filter(
                M.Proxy.expire > expire,
                M.Proxy.location_id == location_id,
                M.Proxy.type_id == type_id)
            result = await session.execute(stmt)
            return result.mappings().all()
