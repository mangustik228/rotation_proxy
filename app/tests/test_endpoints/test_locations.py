import pytest
from httpx import AsyncClient
from tests.utils import LocationBuilder


async def test_get_locations(client: AsyncClient):
    response = await client.get("/locations")
    assert response.status_code == 200
    data = response.json()
    assert len(data["locations"]) == 1


async def test_get_one_location(client: AsyncClient):
    response = await client.get("/locations/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Russia"


async def test_post_location(client: AsyncClient, clear_db):
    location = LocationBuilder().build()
    response = await client.post("/locations", json=location)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "created"
    assert data["location"]["name"] == "Cambodia"


async def test_post_location_dublicates(client: AsyncClient, clear_db):
    location = LocationBuilder().build()
    for _ in range(2):
        response = await client.post("/locations", json=location)
    assert response.status_code == 409


async def test_post_few_locations(client: AsyncClient, clear_db):
    builder = LocationBuilder()
    for i in range(10):
        builder.set_name(f"{chr(97 + i)}")
        location = builder.build()
        response = await client.post("/locations", json=location)
        assert response.status_code == 201
    response = await client.get("/locations")
    data = response.json()
    assert len(data["locations"]) == 11


async def test_put_location(client: AsyncClient, clear_db):
    location = LocationBuilder().build()
    response = await client.put("/locations/1", json=location)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "updated"
    assert data["location"]["name"] == "Cambodia"

    response = await client.get("/locations/1")
    data = response.json()
    assert data["name"] == "Cambodia"


async def test_put_location_error(client: AsyncClient, clear_db):
    location = LocationBuilder().build()
    response = await client.put("/locations/2", json=location)

    assert response.status_code == 404
