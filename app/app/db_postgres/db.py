from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config.config import settings


class Base(DeclarativeBase):
    ...


DATABASE_PARAMS = {"poolclass": NullPool} if settings.MODE == "TEST" else {}


engine = create_async_engine(settings.db.url, **DATABASE_PARAMS)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
