from fastapi.testclient import TestClient
from tests.utils import ProxyTypesBuilder


def test_get_list(client: TestClient):
    response = client.get("/types")
    assert response.status_code == 200
    data = response.json()
    assert len(data["types"]) == 1


def test_get_one(client: TestClient):
    response = client.get("/types/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "IPv4"


def test_get_one_empty(client: TestClient):
    response = client.get("/types/2")
    assert response.status_code == 404


def test_post_proxy(client: TestClient, sql_clear):
    proxy_type = ProxyTypesBuilder().build()
    response = client.post("/types", json=proxy_type)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "created"
    assert data["type"]["name"] == "IPv6"


def test_post_proxy_dublicates(client: TestClient, sql_clear):
    proxy_type = ProxyTypesBuilder().build()
    for i in range(2):
        response = client.post("/types", json=proxy_type)
    assert response.status_code == 409


def test_put_proxy(client: TestClient, sql_clear):
    proxy_type = ProxyTypesBuilder().build()
    response = client.put("/types/1", json=proxy_type)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "updated"
    assert data["type"]["name"] == "IPv6"


def test_put_proxy_empty(client: TestClient, sql_clear):
    proxy_type = ProxyTypesBuilder().build()
    response = client.put("/types/2", json=proxy_type)
    assert response.status_code == 404


def test_put_get_proxy(client: TestClient, sql_clear):
    builder = ProxyTypesBuilder()
    proxy_type_name = "shared"
    builder.set_name(proxy_type_name)
    data = builder.build()
    response = client.put("/types/1", json=data)
    assert response.status_code == 201

    response = client.get("/types/1")
    data = response.json()
    assert data["name"] == proxy_type_name
