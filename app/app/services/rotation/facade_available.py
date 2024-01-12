import app.repo as R
import app.schemas as S
from app.exceptions import NotAvailableProxies

from .facade_base import FacadeRotationBase


class FacadeRotationAvailable(FacadeRotationBase):
    def __init__(self, parsed_service: str,
                 count: int,
                 expire_proxy: str | None,
                 location_id: int | None,
                 type_id: int,
                 lock_time: int):
        self.parsed_service = parsed_service  # look setter
        self.expire_proxy = expire_proxy  # look setter
        self.location_id = location_id
        self.type_id = type_id
        self.count = count
        self.lock_time = lock_time

    async def prepare_proxies(self):
        '''Проверяет если вообще актуальные прокси'''
        data = []
        self._result = {}
        self._result["data"] = data
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if not await self.is_free_in_redis(proxy, self.parsed_service):
                continue
            data.append(proxy)
            await R.ProxyBusy.add(proxy.id, self.lock_time)
            if len(data) == self.count:
                self._result["status"] = "full"
                break
        if not self._result.get("status"):
            self._result["status"] = "not full"
        if len(data) == 0:
            raise NotAvailableProxies("Proxies exist, but none are available")

    @property
    def result(self):
        return self._result
