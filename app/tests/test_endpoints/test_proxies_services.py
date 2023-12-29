from tests.utils import ProxyServiceBuilder
from fastapi.testclient import TestClient


def test_get_services(client: TestClient):
    result = client.get("/services")
    assert result.status_code == 200
    assert len(result.json()) == 1


def test_post_services(client: TestClient, clear_db):
    builder = ProxyServiceBuilder()
    builder.set_name("hello world")
    service = builder.build()
    result = client.post("/services", json=service)
    assert result.status_code == 201
    assert result.json()["service"]["name"] == "hello world"
    assert result.json()["service"]["id"] == 2


def test_post_services_dublicates(client: TestClient, clear_db):
    service = ProxyServiceBuilder().build()
    for _ in range(2):
        result = client.post("/services", json=service)
    assert result.status_code == 409


def test_put_services(client: TestClient, clear_db):
    builder = ProxyServiceBuilder()
    builder.set_name("world")
    service = builder.build()
    response = client.put("/services/1", json=service)
    assert response.status_code == 201


def test_get_one(client: TestClient):
    response = client.get("/services/1")
    assert response.status_code == 200


def test_get_one_empty(client: TestClient):
    response = client.get("/services/2")
    assert response.status_code == 404
