import app.repo as R
import app.schemas as S
from app.exceptions import NotAvailableProxies

from .facade_base import FacadeRotationBase


class FacadeRotationPatch(FacadeRotationBase):
    def __init__(self,
                 id: int,
                 parsed_service: str,
                 parsed_service_id: int,
                 ignore_hours: int,
                 expire_proxy: int,
                 location_id: int,
                 type_id: int,
                 lock_time: int,
                 reason: str,
                 params: dict,
                 logic: int):
        self.id = id
        self.parsed_service = parsed_service  # look parent property
        self.parsed_service_id = parsed_service_id
        self.ignore_hours = ignore_hours
        self.expire_proxy = expire_proxy  # look parent property
        self.location_id = location_id
        self.type_id = type_id
        self.lock_time = lock_time  # For buzy
        self.reason = reason
        self.params = params
        self.logic = logic

    async def prepare_proxy(self) -> S.AvailableProxy:
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if await self.is_free_in_redis(proxy, self.parsed_service):
                await R.ProxyBusy.add(proxy.id, expire=self.lock_time)
                return proxy
        raise NotAvailableProxies("not availalbe proxy")
