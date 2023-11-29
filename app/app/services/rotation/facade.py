import random
import sqlalchemy as sa
import app.schemas as S
import app.repo as R


class FacadeRotation:
    @classmethod
    def shuffle_proxies(cls, proxies: list):
        random.shuffle(proxies)

    @classmethod
    async def prepare_proxies(cls,
                              proxies: list[sa.RowMapping],
                              parsing_service: str,
                              count: int):
        result = []
        for model_proxy in proxies:
            proxy = S.AvailableProxy(**model_proxy)
            if await R.ProxyBlocked.exist(proxy.view(parsing_service)):
                print("not exist")

            result.append(proxy)
            if len(result) == count:
                return result
            # S.AvailableProxy()
        return result
