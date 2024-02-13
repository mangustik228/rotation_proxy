from datetime import datetime, timezone

from httpx import AsyncClient
from loguru import logger

import app.schemas as S
from app.exceptions import NotAvailableProxiesInService, ProblemWithService


class ProxyNetService:
    def __init__(self, url: str, api_key: str):
        self.url = f"{url}{api_key}/getproxy"
        self.params = {
            "api_key": api_key,
            "status": "active"
        }

    async def get_proxies(self):
        async with AsyncClient() as client:
            response = await client.get(self.url, params=self.params)
            if response.status_code == 200:
                data = response.json()
                if data["list_count"] == 0:
                    raise NotAvailableProxiesInService(
                        "SpaceProxy have no actual proxies")
                return self._extract_proxies(data["list"])
            else:
                raise ProblemWithService(
                    f'status code: {response.status_code}')

    def _extract_proxies(self, data: dict[str, dict]):
        result = []

        for datum in data.values():
            proxy = {}
            proxy["expire"] = datetime.fromtimestamp(datum["unixtime_end"])
            proxy["server"] = datum["host"]
            proxy["username"] = datum["user"]
            proxy["password"] = datum["pass"]
            proxy["port"] = datum["port"]
            proxy["location_id"] = 1  # TODO
            proxy["service_id"] = 3
            proxy["type_id"] = 1  # TODO
            result.append(S.PostRequestProxy(**proxy))
        return result
