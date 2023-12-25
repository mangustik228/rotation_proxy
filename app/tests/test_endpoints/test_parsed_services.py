from httpx import AsyncClient


async def test_get_one(insert_parsed_services, client: AsyncClient):
    response = await client.get("/parsed_services/1")
    assert response.status_code == 200
    assert response.json()["name"] == "example-service"


async def test_get_one_empty(client: AsyncClient):
    response = await client.get("/parsed_services/1")
    assert response.status_code == 404


async def test_get_list(insert_parsed_services, client: AsyncClient):
    response = await client.get("/parsed_services")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["parsed_services"]) == 2
    assert data["count"] == 2


async def test_post_service(clear_db, client: AsyncClient):
    data = {"name": "example-service"}
    response = await client.post("/parsed_services", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["status"] == "created"
    assert result["parsed_service"]["id"] == 1


async def test_post_service_error(clear_db, client: AsyncClient):
    data = {"name": "example-service"}
    for _ in range(2):
        response = await client.post("/parsed_services", json=data)
    assert response.status_code == 409


async def test_get_by_name(insert_parsed_service, client: AsyncClient):
    params = {"name": "example-service"}
    response = await client.get("/parsed_services/name", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "exist"
    assert data["id"] == 1
