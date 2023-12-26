from app.db_postgres import async_session
import app.repo as R
from sqlalchemy import text


async def test_get_name_by_id(insert_parsed_service):
    name = await R.ParsedService.get_name_by_id(1)
    q = 'select * from parsed_service'
    async with async_session() as session:
        result = await session.execute(text(q))
        print(result.mappings().all())
    assert name == "example-service"
