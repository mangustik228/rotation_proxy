from fastapi import APIRouter, HTTPException, status, Body
import app.schemas as S
import app.repo as R
from app.exceptions import NotValidExpire, NotValidServiceName, NotAvailableProxies
from app.services import FacadeRotationAvailable, FacadeRotationPatch, CalculateDelay
from loguru import logger

router = APIRouter(prefix="/proxies/rotations", tags=["ROTATIONS"])


@router.get("", response_model=S.GetResponseAvailableProxy)
async def get_available(
        parsed_service_id: int,
        parsed_service: str | None = None,
        count: int = 5,
        location_id: int | None = 1,
        type_id: int | None = 1,
        lock_time: int | None = 300,
        expire_proxy: str | None = None):
    if parsed_service is None:
        parsed_service = await R.ParsedService.get_name_by_id(parsed_service_id)
    try:
        facade = FacadeRotationAvailable(
            parsed_service=parsed_service,
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
    except NotAvailableProxies as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return facade.result


# , response_model=S.PatchResponseAvailableProxy
@router.patch("")
async def change_proxy(data: S.PatchRequestAvailableProxy = Body()):
    if parsed_service is None:
        parsed_service = await R.ParsedService.get_name_by_id(data.parsed_service_id)
    else:
        parsed_service = data.parsed_service
    facade = FacadeRotationPatch(
        **data.dump_to_facade(), parsed_service=parsed_service)
    await facade.get_available_from_sql()
    # Смотрим прошлые баны
    last_blocks = await R.Error.get_last_5(
        data.id,
        data.ignore_blocks_older_then_hours)
    # Высчитываем сколько должен быть блок
    params = data.params if data.params else {}
    calculator = CalculateDelay(data.logic, last_blocks, params)
    delay = calculator.calculate_time()

    result = await facade.prepare_proxy()
    return result
