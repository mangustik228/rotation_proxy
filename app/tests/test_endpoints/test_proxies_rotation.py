from httpx import AsyncClient
import pytest
from tests.utils import ProxyServiceBuilder


@pytest.mark.skip
async def test_get_available_proxies_404(client: AsyncClient):
    params = {
        "parsing_service": "example"
    }
    response = await client.get("/proxies/rotations", params=params)
    assert response.status_code == 404, response.text
