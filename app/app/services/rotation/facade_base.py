import sqlalchemy as sa
import app.repo as R
import random
from app.exceptions import NotAvailableProxies, NotValidServiceName, NotValidServiceName, NotValidExpire
from datetime import datetime, timedelta
from pydantic import ValidationError
import app.schemas as S


class FacadeRotationBase:
    def __init__(self, parsed_service: str,
                 count: int,
                 expire_proxy: str | None,
                 location_id: int,
                 type_id: int,
                 lock_time: int):
        self.parsed_service = parsed_service  # look setter
        self.expire_proxy = expire_proxy  # look setter
        self.location_id = location_id
        self.type_id = type_id
        self.count = count
        self.lock_time = lock_time

    async def get_available_from_sql(self):
        self.proxies_models: list[sa.RowMapping] = await R.Proxy.get_available(
            self.expire_proxy, self.location_id, self.type_id)
        if len(self.proxies_models) == 0:
            raise NotAvailableProxies("Нет актуальных прокси")
        random.shuffle(self.proxies_models)

    @property
    def parsed_service(self):
        return self._service

    @parsed_service.setter
    def parsed_service(self, other):
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

    async def is_free_in_redis(self, proxy: S.AvailableProxy):
        if await R.ProxyBlocked.is_not_free(proxy.id, self.parsed_service):
            return False
        if await R.ProxyBuzy.is_not_free(proxy.id):
            return False
        return True
