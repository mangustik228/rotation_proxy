from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config.config import settings


class Base(DeclarativeBase):
    ...


DATABASE_PARAMS = {"poolclass": NullPool} if settings.MODE == "TEST" else {}


engine = create_async_engine(settings.db.url, **DATABASE_PARAMS)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
