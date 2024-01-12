from .facade_base import FacadeRotationBase
import app.schemas as S
import app.repo as R
from app.exceptions import NotAvailableProxies


class FacadeSimpleChange(FacadeRotationBase):

    async def get_free_proxy(self):
        '''Проверяет если вообще актуальные прокси'''
        for model_proxy in self.proxies_models:
            proxy = S.AvailableProxy(**model_proxy)
            if not await self.is_free_in_redis(proxy, self.parsed_service):
                continue
            await R.ProxyBusy.add(proxy.id, self.lock_time)
            return proxy
        raise NotAvailableProxies("Proxies exist, but none are available")

    async def free_old_proxy(self, proxy_id: int):
        await R.ProxyBusy.free(proxy_id)
