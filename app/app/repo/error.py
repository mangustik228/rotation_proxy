from .base_repo import BaseRepo
import app.models as M
from app.db_postgres import async_session
from sqlalchemy import select


class Error(BaseRepo):
    model = M.Error

    @classmethod
    async def get_last_5(cls, id: int):
        async with async_session() as session:
            stmt = select(cls.model)\
                .where(cls.model.id == id)\
                .order_by(cls.model.created_at)\
                .limit(5)
            result = await session.execute(stmt)
            return result.mappings().all()
