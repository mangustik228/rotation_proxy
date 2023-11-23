import asyncio
from loguru import logger
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db_postgres import async_session
import app.models as M
from app.exceptions import DuplicateKey


def check_alchemy_problem(func: asyncio.coroutine):
    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            if "duplicate key" in e._sql_message():
                logger.info("Value is already exist")
                raise DuplicateKey("Value is already exist")
        except Exception as e:
            logger.error(str(e))

    return inner


class BaseRepo:
    model = None

    @classmethod
    async def get_by_id(cls, id: int):
        logger.info(f'GET by id: {id}')
        async with async_session() as session:
            stmt = select(cls.model).where(cls.model.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls):
        logger.info(f'[{cls.__name__}] get all')
        async with async_session() as session:
            stmt = select(cls.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, count, **filter_by):
        logger.info(f"[{cls.__name__}] try to find count: {count}")
        async with async_session() as session:
            stmt = select(cls.model).filter_by(*filter_by).limit(count)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    @check_alchemy_problem
    async def add_one(cls, **data) -> int:
        logger.info(f"[{cls.__name__}] try to add one: {data}")
        async with async_session() as session:
            async with session.begin():
                stmt = insert(cls.model).values(
                    **data).returning(cls.model)
                result = await session.execute(stmt)
                result = result.scalar()
                await session.commit()
                return result

    @classmethod
    async def delete(cls, **filter_by):
        logger.info(f"[{cls.__name__}] try to add delete: {filter_by}")
        async with async_session() as session:
            stmt = delete(cls.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    @check_alchemy_problem
    async def update(cls, id: int, **data):
        logger.info(f"[{cls.__name__}] try to add update id=[{id}]: {data}")
        async with async_session() as session:
            async with session.begin():
                stmt = update(cls.model).where(cls.model.id == id).values(
                    **data).returning(cls.model)
                result = await session.execute(stmt)
                result = result.scalar()
                await session.commit()
                return result
