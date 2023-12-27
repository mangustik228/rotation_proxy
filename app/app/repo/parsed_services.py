from sqlalchemy import select
from .base_repo import BaseRepo
import app.models as M
from app.db_postgres import async_session
from app.exceptions import NotExistedParsedService, NotValidServiceName
from .base_repo import check_alchemy_problem


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
            parsed_service_name = result.scalar_one_or_none()
        if parsed_service_name is None:
            raise NotExistedParsedService(
                f"Parsed_service with id: {id} doesn't exist")
        return parsed_service_name

    @classmethod
    async def add_one(cls, **data) -> M.ParsedService:
        if "_" in data["name"]:
            raise NotValidServiceName
        return await super().add_one(**data)
