import pytest
from fastapi.testclient import TestClient
from tests.utils import LocationBuilder


def test_get_locations(client: TestClient):
    response = client.get("/locations")
    assert response.status_code == 200
    data = response.json()
    assert len(data["locations"]) == 2


@pytest.mark.parametrize("id,expected,expected_parent_id",
                         [(1, "Russia", None), (2, "Moscow", 1)])
def test_get_one_location(client: TestClient, id, expected, expected_parent_id):
    response = client.get(f"/locations/{id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == expected
    assert data["parent_id"] == expected_parent_id


def test_post_location(client: TestClient, sql_clear):
    location = LocationBuilder().build()
    response = client.post("/locations", json=location)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "created"
    assert data["location"]["name"] == "Cambodia"


def test_post_location_dublicates(client: TestClient, sql_clear):
    location = LocationBuilder().build()
    for _ in range(2):
        response = client.post("/locations", json=location)
    assert response.status_code == 409


def test_post_few_locations(client: TestClient, sql_clear):
    builder = LocationBuilder()
    for i in range(10):
        builder.set_name(f"{chr(97 + i)}")
        location = builder.build()
        response = client.post("/locations", json=location)
        assert response.status_code == 201
    response = client.get("/locations")
    data = response.json()
    assert len(data["locations"]) == 12


def test_put_location(client: TestClient, sql_clear):
    location = LocationBuilder().build()
    response = client.put("/locations/1", json=location)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "updated"
    assert data["location"]["name"] == "Cambodia"

    response = client.get("/locations/1")
    data = response.json()
    assert data["name"] == "Cambodia"


def test_put_location_error(client: TestClient, sql_clear):
    location = LocationBuilder().build()
    response = client.put("/locations/3", json=location)

    assert response.status_code == 404
