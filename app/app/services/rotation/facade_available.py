from datetime import datetime, timedelta
import random
import sqlalchemy as sa
import app.schemas as S
import app.repo as R
from app.exceptions import NotValidServiceName, NotValidExpire, NoAvailableProxies
from pydantic import ValidationError


class FacadeRotationAvailable:
    def __init__(self, service: str,
                 count: int,
                 expire_proxy: str,
                 location_id: int,
                 type_id: int,
                 lock_time: int):
        self.service = service  # look setter
        self.expire_proxy = expire_proxy  # look setter
        self.location_id = location_id
        self.type_id = type_id
        self.count = count
        self.lock_time = lock_time

    async def get_available_from_sql(self):
        self.proxies_models: list[sa.RowMapping] = await R.Proxy.get_available(
            self.expire_proxy, self.location_id, self.type_id)
        if len(self.proxies_models) == 0:
            raise NoAvailableProxies("Нет актуальных прокси")

    def shuffle_proxies_from_sql(self):
        random.shuffle(self.proxies_models)

    async def prepare_proxies(self):
        data = []
        self._result = {}
        self._result["data"] = data
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if await R.ProxyBlocked.is_blocked_by_service(proxy.id, self.service):
                continue
            if await R.ProxyBuzy.is_busy(proxy.id):
                continue
            data.append(proxy)
            await R.ProxyBuzy.add(proxy.id, self.lock_time)
            R.ProxyBuzy
            if len(data) == self.count:
                self._result["status"] = "full"
                break
        if not self._result.get("status"):
            self._result["status"] = "not full"
        if len(data) == 0:
            raise NoAvailableProxies("Proxies exist, but none are available")

    @property
    def result(self):
        return self._result

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, other):
        if "_" in other:
            raise NotValidServiceName("service name couldn't exist '_'")
        self._service = other

    @property
    def expire_proxy(self):
        return self._expire

    @expire_proxy.setter
    def expire_proxy(self, other):
        if other is None:
            self._expire = datetime.now().replace(
                second=0, microsecond=0) + timedelta(days=1)
            return
        try:
            self._expire = S.ValidateDate(date=other).date
        except ValidationError:
            raise NotValidExpire(
                "expire must be format '2023-12-01T00:00:00` or None")
