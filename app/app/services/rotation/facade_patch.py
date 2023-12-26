from .facade_base import FacadeRotationBase
import app.schemas as S
import app.repo as R
from app.exceptions import NotAvailableProxies


class FacadeRotationPatch(FacadeRotationBase):
    def __init__(self,
                 id: int,
                 parsed_service: str,
                 parsed_service_id: int,
                 ignore_blocks_older_then_hours: int,
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
        self.ignore_blocks_older_then_hours = ignore_blocks_older_then_hours
        self.expire_proxy = expire_proxy  # look parent property
        self.location_id = location_id
        self.type_id = type_id
        self.lock_time = lock_time
        self.reason = reason
        self.params = params
        self.logic = logic

    async def prepare_proxy(self) -> S.AvailableProxy:
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if await self.is_free_in_redis(proxy):
                return proxy
        raise NotAvailableProxies("not availalbe proxy")
