from .facade_base import FacadeRotationBase
import app.schemas as S
import app.repo as R


class FacadeRotationPatch(FacadeRotationBase):
    async def prepare_proxy(self) -> S.AvailableProxy:
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if self.is_free_in_redis(proxy):
                return proxy
