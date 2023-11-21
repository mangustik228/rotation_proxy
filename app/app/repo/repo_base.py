import json
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db_postgres import async_session
import app.models as M
from loguru import logger


class BaseRepo:
    model = None

    @classmethod
    async def find_one_or_none(cls, count, **filter_by):
        logger.info(f"[{cls.__name__}] try to find count: {count}")
        async with async_session() as session:
            stmt = select(cls.model).filter_by(*filter_by).limit(count)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def add_one(cls, **data) -> int:
        logger.info(f"[{cls.__name__}] try to add one: {data}")
        async with async_session() as session:
            async with session.begin():
                try:
                    stmt = insert(cls.model).values(
                        **data).returning(cls.model.id)
                    result = await session.execute(stmt)
                    await session.commit()
                    return result.scalar()
                except IntegrityError as e:
                    logger.info(f"couldn't set data [{data}] ({str(e)})")

    @classmethod
    async def delete(cls, **filter_by):
        logger.info(f"[{cls.__name__}] try to add delete: {filter_by}")
        async with async_session() as session:
            stmt = delete(cls.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update(cls, id: int, **data):
        logger.info(f"[{cls.__name__}] try to add update id=[{id}]: {data}")
        async with async_session() as session:
            stmt = update(cls.model).where(cls.model.id == id).values(**data)
            await session.execute(stmt)
            await session.commit()
