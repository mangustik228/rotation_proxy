from app.db_postgres import async_session
import app.repo as R
from sqlalchemy import text
import pytest
from app.exceptions import NotValidServiceName, DuplicateKey


async def test_get_name_by_id(insert_parsed_service):
    name = await R.ParsedService.get_name_by_id(1)
    assert name == "example-service"


async def test_insert_service(clear_db):
    data = {"name": "example-parsed-service"}
    result = await R.ParsedService.add_one(**data)
    assert result.id == 1
    assert result.name == "example-parsed-service"


async def test_insert_service_not_valid_name(clear_db):
    data = {"name": "example_parsed-service"}
    with pytest.raises(NotValidServiceName):
        await R.ParsedService.add_one(**data)


async def test_get_by_name(insert_parsed_service):
    result = await R.ParsedService.get_by_name("example-service")
    assert result == 1
