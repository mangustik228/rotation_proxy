from fastapi.testclient import TestClient


def test_get_one(insert_parsed_services, client: TestClient):
    response = client.get("/parsed_services/1")
    assert response.status_code == 200
    assert response.json()["name"] == "example-service"


def test_get_one_empty(client: TestClient):
    response = client.get("/parsed_services/1")
    assert response.status_code == 404


def test_get_list(insert_parsed_services, client: TestClient):
    response = client.get("/parsed_services")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["parsed_services"]) == 2
    assert data["count"] == 2


def test_post_service(clear_db, client: TestClient):
    data = {"name": "example-service"}
    response = client.post("/parsed_services", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["status"] == "created"
    assert result["parsed_service"]["id"] == 1


def test_post_service_error(clear_db, client: TestClient):
    data = {"name": "example-service"}
    for _ in range(2):
        response = client.post("/parsed_services", json=data)
    assert response.status_code == 409


def test_get_by_name(insert_parsed_service, client: TestClient):
    params = {"name": "example-service"}
    response = client.get("/parsed_services/name", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "exist"
    assert data["id"] == 1
