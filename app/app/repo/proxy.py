from datetime import date
from loguru import logger
from sqlalchemy import select
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from .repo_base import BaseRepo
import app.models as M
import app.schemas as S
from app.db_postgres import async_session


class Proxy(BaseRepo):
    model = M.Proxy

    @classmethod
    async def add_many(cls, data: list[S.ProxyBase]):
        values = [M.Proxy(**item.model_dump()) for item in data]
        async with async_session() as session:
            session.add_all(values)
            try:
                await session.commit()
                return "success"
            except UniqueViolationError as e:
                logger.warning("Пытались вставить дубли")
                return "Судя по всему дубли. такие данные уже существуют"
            except Exception as e:
                logger.warning(repr(e))
                return repr(e)

    @classmethod
    async def get_all(cls, count: int):
        async with async_session() as session:
            stmt = select(cls.model)\
                .where(M.Proxy.expire > date.today())\
                .limit(count)
            proxies = await session.execute(stmt)
            proxies = proxies.scalars().all()
            return proxies
