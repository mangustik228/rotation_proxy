from fastapi import APIRouter, HTTPException, status, Body
import app.schemas as S
import app.repo as R
from app.exceptions import NotValidExpire, NotValidServiceName, NoAvailableProxies
from app.services import FacadeRotationAvailable, FacadeRotationPatch

router = APIRouter(prefix="/proxies/rotations", tags=["ROTATIONS"])


@router.get("", response_model=S.GetResponseAvailableProxy)
async def get_available(
        parsing_service: str,
        count: int = 5,
        location_id: int | None = 1,
        type_id: int | None = 1,
        lock_time: int | None = 300,
        expire_proxy: str | None = None):
    try:
        facade = FacadeRotationAvailable(
            service=parsing_service,
            count=count,
            expire_proxy=expire_proxy,
            location_id=location_id,
            type_id=type_id,
            lock_time=lock_time)
        await facade.get_available_from_sql()
        await facade.prepare_proxies()
    except NotValidExpire as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    except NotValidServiceName as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    except NoAvailableProxies as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return facade.result


@router.patch("", response_model=S.PatchResponseAvailableProxy)
async def change_proxy(data: S.PatchRequestAvailableProxy = Body()):
    try:
        facade = FacadeRotationPatch(**data.model_dump())
        await facade.get_available_from_sql()
        last_blocks = await R.Error.get_last_5(data.id)
        return await facade.prepare_proxy()
    except:
        ...
