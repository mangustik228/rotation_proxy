import app.schemas as S
import app.repo as R
from app.exceptions import NotAvailableProxies
from pydantic import ValidationError
from .facade_base import FacadeRotationBase


class FacadeRotationAvailable(FacadeRotationBase):
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

    async def prepare_proxies(self):
        data = []
        self._result = {}
        self._result["data"] = data
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if not self.is_free_in_redis(proxy):
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
            raise NotAvailableProxies("Proxies exist, but none are available")

    @property
    def result(self):
        return self._result
