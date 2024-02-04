from datetime import datetime, timezone

from httpx import AsyncClient

import app.schemas as S
from app.exceptions import NotAvailableProxiesInService, ProblemWithService


class SpaceProxyService:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.params = {
            "api_key": api_key,
            "status": "active"
        }

    async def get_proxies(self):
        async with AsyncClient() as client:
            response = await client.get(self.url, params=self.params)
            if response.status_code == 200:
                data = response.json()
                if data["count"] == 0:
                    raise NotAvailableProxiesInService(
                        "SpaceProxy have no actual proxies")
                return self._extract_proxies(data["results"])
            else:
                raise ProblemWithService(
                    f'status code: {response.status_code}')

    def _extract_proxies(self, data: dict):
        result = []
        for datum in data:
            expire = datetime\
                .fromisoformat(datum["date_end"])\
                .astimezone(timezone.utc)\
                .replace(tzinfo=None)

            proxy = {
                "server": datum["ip"],
                "username": datum["username"],
                "password": datum["password"],
                "port": datum["port_http"],
                "location_id": 1,  # TODO
                "type_id": 1,  # TODO
                "country_id": 1,  # TODO
                "service_id": 4,
                "expire": expire
            }
            result.append(S.PostRequestProxy(**proxy))
        return result
