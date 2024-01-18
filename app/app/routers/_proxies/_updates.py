from fastapi import APIRouter
from loguru import logger

import app.repo as R
import app.schemas as S
from app.config import settings
from app.services import ProxyIoService

router = APIRouter(prefix="/updates", tags=["UPDATES"])


@router.patch("/proxy_io", response_model=S.PostResponseProxyList)
async def check_proxy_io():
    logger.debug("come in post")
    proxy_io_service = ProxyIoService(
        url=settings.services.proxy_io.url,
        api_key=settings.services.proxy_io.api_key
    )
    proxies = await proxy_io_service.get_proxies()
    return await R.Proxy.add_many(proxies)
