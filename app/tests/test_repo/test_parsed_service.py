import pytest
from sqlalchemy import text

import app.repo as R
from app.db_postgres import async_session
from app.exceptions import DuplicateKey, NotValidServiceName


async def test_get_name_by_id(sql_insert_parsed_service):
    name = await R.ParsedService.get_name_by_id(1)
    assert name == "example-service"


async def test_insert_service(sql_clear):
    data = {"name": "example-parsed-service"}
    result = await R.ParsedService.add_one(**data)
    assert result.id == 1
    assert result.name == "example-parsed-service"


async def test_insert_service_not_valid_name(sql_clear):
    data = {"name": "example_parsed-service"}
    with pytest.raises(NotValidServiceName):
        await R.ParsedService.add_one(**data)


async def test_get_by_name(sql_insert_parsed_service):
    result = await R.ParsedService.get_by_name("example-service")
    assert result == 1
