from datetime import datetime
from fastapi import HTTPException
from fastapi import APIRouter, status, Body
from loguru import logger
import app.schemas as S
import app.repo as R
from app.services import ProxyFormater
from app.exceptions import DuplicateKey
from .rotations import router as rotation_router

router = APIRouter(prefix="/proxies", tags=["PROXIES"])


@router.get("", response_model=S.GetResponseProxyList)
async def get_all_proxies():
    proxies = await R.Proxy.get_all()
    total_proxies = await R.Proxy.get_total_count()
    active_proxies = await R.Proxy.get_active_count()
    return {
        "total_count": total_proxies,
        "total_active_count": active_proxies,
        "status": "success",
        "proxies": proxies
    }


@router.get("/{id}", response_model=S.GetResponseProxy)
async def get_one_proxie(id: int):
    proxy = await R.Proxy.get_by_id(id)
    return proxy


@router.post("",
             status_code=status.HTTP_201_CREATED)
async def post_proxies(data: S.PostRequestProxy = Body()):
    try:
        result = await R.Proxy.add_one(**data.model_dump())
        return {"status": "success",
                "proxy": result}
    except DuplicateKey:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="proxy is already exist.")


@router.post("/bulk",
             status_code=status.HTTP_201_CREATED,
             response_model=S.PostResponseProxyList)
async def post_bulk_proxies(data: list[S.PostRequestProxy] = Body()):
    success = 0
    errors = 0
    for datum in data:
        try:
            await R.Proxy.add_one(**datum.model_dump())
            success += 1
        except:
            errors += 1
    return {
        "status": "success",
        "count_added": success,
        "count_errors": errors
    }


# @router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_proxy(id: int):
#     ...


# @router.get("")
# async def get_proxies(service: str | None = None,
#                       location_id: int | None = 1,
#                       count: int = 25,
#                       format: str = "short",
#                       app_type: str = "playwright",
#                       expire: datetime = datetime.utcnow(),
#                       type_id: int | None = 1):
#     '''
#     Get current proxies:
#     **format:** Literal["full", "queue", "short"]
#       - full
#         ```python
#         [{
#             "server": "...",
#             "username": "...",
#             "password"" "..."
#         }]
#         ```
#     **app_type:** Literal["requests", "playwright"]

#     '''
#     result = await R.Proxy.get_all(count)
#     try:
#         return ProxyFormater.prepare_proxies(result, format, app_type)
#     except ValueError as e:
#         return HTTPException(422, str(e))


# @router.get("/{id}")
# async def get_proxy(id: int):
#     ...


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_proxy(id: int):
#     ...


# @router.post("/change")
# async def change_proxy(data: S.ProxyBase = Body()):
#     ...
