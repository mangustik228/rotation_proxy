from fastapi import FastAPI

from ._errors import router as error
from ._locations import router as location
from ._parsed_services import router as parsed_services
from ._proxies.base import router as proxies
from ._proxies.blocks import router as proxy_blocks
from ._proxies.busies import router as proxy_busy
from ._proxies.rotations import router as proxies_rotations
from ._proxy_service import router as proxy_service
from ._proxy_type import router as proxy_type


def register_routers(app: FastAPI):
    app.include_router(proxies_rotations)
    app.include_router(parsed_services)
    app.include_router(proxy_blocks)
    app.include_router(proxy_busy)
    app.include_router(proxies)
    app.include_router(proxy_service)
    app.include_router(location)
    app.include_router(proxy_type)
    app.include_router(error)
