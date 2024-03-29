import asyncio

from loguru import logger
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import DataError, IntegrityError

from app.db_postgres import async_session
from app.exceptions import DateNotValidFormat, DuplicateKey, DbProblem
import app.schemas as S


def check_alchemy_problem(func: asyncio.coroutine):
    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            if "duplicate key" in e._sql_message():
                msg = f"Value is already exist {kwargs}"
                # logger.info(msg)
                raise DuplicateKey(msg)
            else:
                raise DbProblem(str(e))
        except DataError as e:
            msg = f"Problem with insert date {kwargs}"
            logger.error(msg)
            raise DateNotValidFormat(msg)
        except Exception as e:
            logger.error(str(e))
            raise DbProblem(str(e))
    return inner


class BaseRepo:
    model = None

    @classmethod
    async def get_id_by_name(cls, name: str) -> int | None:
        # logger.info(f'GET by name: {name}')
        async with async_session() as session:
            stmt = select(cls.model.id).where(
                func.lower(cls.model.name) == func.lower(name))
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, id: int):
        # logger.info(f'GET by id: {id}')
        async with async_session() as session:
            stmt = select(cls.model).where(cls.model.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls):
        # logger.info(f'[{cls.__name__}] get all')
        async with async_session() as session:
            stmt = select(cls.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, count, **filter_by):
        # logger.info(f"[{cls.__name__}] try to find count: {count}")
        async with async_session() as session:
            stmt = select(cls.model).filter_by(*filter_by).limit(count)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    @check_alchemy_problem
    async def add_one(cls, **data) -> int:
        # logger.info(f"[{cls.__name__}] try to add one: {data}")
        async with async_session() as session:
            async with session.begin():
                stmt = insert(cls.model).values(
                    **data).returning(cls.model)
                result = await session.execute(stmt)
                result = result.scalar()
                await session.commit()
                return result

    @classmethod
    async def add_many(cls, proxies: list[S.PostRequestProxy]):
        success = 0
        errors = 0
        for proxy in proxies:
            try:
                await cls.add_one(**proxy.model_dump())
                success += 1
            except DuplicateKey as e:
                errors += 1
        return {
            "status": "created" if success else "not created",
            "count_added": success,
            "count_errors": errors
        }

    @classmethod
    async def delete(cls, **filter_by):
        # logger.info(f"[{cls.__name__}] try to add delete: {filter_by}")
        async with async_session() as session:
            stmt = delete(cls.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    @check_alchemy_problem
    async def update(cls, id: int, **data):
        # logger.info(f"[{cls.__name__}] try to add update id=[{id}]: {data}")
        async with async_session() as session:
            stmt = update(cls.model).where(cls.model.id == id).values(
                **data).returning(cls.model)
            result = await session.execute(stmt)
            result = result.scalar()
            await session.commit()
            return result

    @classmethod
    async def count_items(cls):
        async with async_session() as session:
            stmt = select(func.count()).select_from(cls.model)
            result = await session.execute(stmt)
            return result.scalar_one()
