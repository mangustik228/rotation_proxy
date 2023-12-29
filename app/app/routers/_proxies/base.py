from fastapi import HTTPException
from fastapi import APIRouter, status, Body
from loguru import logger
import app.schemas as S
import app.repo as R
from app.exceptions import DuplicateKey

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
    except DuplicateKey as e:
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
        except DuplicateKey as e:
            errors += 1
    return {
        "status": "created",
        "count_added": success,
        "count_errors": errors
    }


@router.put("/{id}", status_code=201, response_model=S.PutResponseProxy)
async def update_proxy(id: int, data: S.PutRequestProxy):
    try:
        result = await R.Proxy.update(id, **data.model_dump())
        if result:
            return {
                "status": "updated",
                "proxy": result
            }
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "proxy not founded")
    except DuplicateKey as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proxy(id: int):
    result = await R.Proxy.get_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="proxy doesn't exist")
    else:
        await R.Proxy.delete(id=id)


@router.patch("/{id}", response_model=S.PatchResponseProxy)
async def patch_proxy(id: int, data: S.PatchRequestProxy = Body()):
    try:
        result = await R.Proxy.update_fields(id, **data.model_dump(exclude_unset=True))
    except DuplicateKey as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e))
    return {"status": "updated", "proxy": result}
