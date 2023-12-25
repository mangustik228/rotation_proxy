from sqlalchemy import select
from .base_repo import BaseRepo
import app.models as M
from app.db_postgres import async_session


class ParsedService(BaseRepo):
    model = M.ParsedService

    @classmethod
    async def get_by_name(cls, name: str) -> int | None:
        async with async_session() as session:
            stmt = select(cls.model.id).where(cls.model.name == name)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
