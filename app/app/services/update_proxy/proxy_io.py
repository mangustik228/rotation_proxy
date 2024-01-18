from datetime import datetime

from httpx import AsyncClient
from loguru import logger

import app.schemas as S
from app.config import settings
from app.exceptions import (NoIdentifyCountryCode, NoIdentifyTypeId,
                            ProblemWithService)


class ProxyIoService:
    def __init__(self, url: str, api_key):
        self.params = {"key": api_key}
        self.url = url

    async def get_proxies(self) -> list[S.PostRequestProxy]:
        async with AsyncClient() as client:
            response = await client.get(self.url, params=self.params)
            if response.status_code == 200:
                data = response.json()
                return self._extract_proxies(data["data"])
            else:
                raise ProblemWithService(
                    f'status_code: {response.status_code}')

    @staticmethod
    def _get_template(order: dict) -> dict:
        template = {}
        template["password"] = order["password"]
        template["username"] = order["username"]
        template["service_id"] = 1
        template["expire"] = datetime.fromtimestamp(order["expires_at"])
        if str(order["ip_version"]) == "4":
            template["type_id"] = 1
        elif str(order["ip_version"]) == "6":
            template["type_id"] = 2
        else:
            raise NoIdentifyTypeId(
                f"у заказа не поддерживаемый протокол. {order['ip_version']}")

        if order["country_code"] == "RU":
            template["location_id"] = 1
        else:
            raise NoIdentifyCountryCode(
                f"Не поддерживаемый код страны {order['country_code']}")
        return template

    def _extract_proxies(self, orders: dict):
        result = []
        for order in orders:
            template = self._get_template(order)
            proxies = self._extract_proxies_with_full_information(
                order, template)
            result.extend(proxies)
        return result

    @staticmethod
    def _extract_proxies_with_full_information(order: dict, template: dict):
        data = []
        for proxy in order["list_ip"]:
            result = template.copy()
            result["server"] = proxy["ip"]
            result["port"] = proxy["port_http"]
            data.append(S.PostRequestProxy(**result))
        return data
