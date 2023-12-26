from sqlalchemy import select
from .base_repo import BaseRepo
import app.models as M
from app.db_postgres import async_session
from app.exceptions import NotExistedParsedService


class ParsedService(BaseRepo):
    model = M.ParsedService

    @classmethod
    async def get_by_name(cls, name: str) -> int | None:
        async with async_session() as session:
            stmt = select(cls.model.id).where(cls.model.name == name)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_name_by_id(cls, id: int) -> str | None:
        async with async_session() as session:
            stmt = select(cls.model.name).where(cls.model.id == id)
            result = await session.execute(stmt)
            parsed_service_id = result.scalar_one_or_none()
        if parsed_service_id is None:
            raise NotExistedParsedService(
                f"Parsed_service with id: {id} doesn't exist")
        return parsed_service_id
