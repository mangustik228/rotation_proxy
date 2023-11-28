from datetime import datetime
from loguru import logger
from sqlalchemy import select, func
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from .base_repo import BaseRepo, check_alchemy_problem
import app.models as M
import app.schemas as S
from app.db_postgres import async_session
from sqlalchemy.orm import selectinload


class Proxy(BaseRepo):
    model = M.Proxy

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            stmt = \
                select(M.Proxy)\
                .where(M.Proxy.id == 1)\
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
            return result.scalar()

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

    # @classmethod
    # @check_alchemy_problem
    # async def add_many(cls, data: list[S.ProxyBase]):
    #     values = [M.Proxy(**item.model_dump()) for item in data]
    #     async with async_session() as session:
    #         async with session.begin():
    #             session.add_all(values)
    #             await session.commit()
    #             return "success"

    # @classmethod
    # async def get_all(cls, count: int):
    #     async with async_session() as session:
    #         stmt = select(cls.model)\
    #             .where(M.Proxy.expire > date.today())\
    #             .limit(count)
    #         proxies = await session.execute(stmt)
    #         proxies = proxies.scalars().all()
    #         return proxies
