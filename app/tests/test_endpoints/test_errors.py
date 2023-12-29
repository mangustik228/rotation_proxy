from fastapi.testclient import TestClient
from tests.utils import ErrorBuilder


def test_post_errors(sql_insert_parsed_service, client: TestClient):
    data = ErrorBuilder().build()
    response = client.post("/errors", json=data)
    assert response.status_code == 201, response.json()
    result = response.json()
    assert result["status"] == "created"
    assert result["error_id"] == 1


def test_post_errors_wrong_status(client: TestClient):
    builder = ErrorBuilder()
    builder.set_proxy_id(100)
    data = builder.build()
    response = client.post("/errors", json=data)
    assert response.status_code == 404


def test_get_errors_by_proxy_id(sql_insert_3_errors, client: TestClient):
    response = client.get("/errors/proxy/1")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert result["count"] == 3
    assert result["proxy"]["id"] == 1


def test_get_errors_by_proxy_id_exception(client: TestClient):
    response = client.get("/errors/proxy/1")
    assert response.status_code == 404


def test_get_errors_by_parsed_service(sql_insert_3_errors, client: TestClient):
    response = client.get("/errors/parsed_service/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 3
    assert data["parsed_service"]["id"] == 1
    assert data["parsed_service"]["name"] == "example-service"
