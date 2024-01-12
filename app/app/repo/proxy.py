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
    @redis_cache
    async def get_available(cls, expire: datetime, location_id: int | None, type_id: int):
        async with async_session() as session:
            if location_id is None:
                stmt = select(
                    M.Proxy.id,
                    M.Proxy.server,
                    M.Proxy.port,
                    M.Proxy.username,
                    M.Proxy.password,
                ).filter(
                    M.Proxy.expire > expire,
                    M.Proxy.type_id == type_id)
            else:
                location_cte = select(M.Location.id)\
                    .where(M.Location.id == location_id)\
                    .cte(recursive=True)
                location_cte = location_cte\
                    .union_all(
                        select(M.Location.id)
                        .join(location_cte, M.Location.parent_id == location_cte.c.id)
                    )

                stmt = select(
                    M.Proxy.id,
                    M.Proxy.server,
                    M.Proxy.port,
                    M.Proxy.username,
                    M.Proxy.password,
                ).filter(
                    M.Proxy.expire > expire,
                    M.Proxy.location_id.in_(select(location_cte.c.id)),
                    M.Proxy.type_id == type_id)
            result = await session.execute(stmt)
            return result.mappings().all()

    @classmethod
    async def get_active_by_services(cls):
        async with async_session() as session:
            stmt = select(M.Service.name, func.count())\
                .select_from(cls.model)\
                .group_by(M.Service.name)\
                .join(M.Service)
            result = await session.execute(stmt)
            return result.mappings().all()
