from fastapi import APIRouter, HTTPException, status, Body
from app.exceptions.exceptions import DuplicateKey
import app.schemas as S
import app.repo as R
from app.exceptions import NotValidExpire, NotValidServiceName, NotAvailableProxies, NotExistedParsedService
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
    facade = FacadeRotationAvailable(
        parsed_service=parsed_service,
        count=count,
        expire_proxy=expire_proxy,
        location_id=location_id,
        type_id=type_id,
        lock_time=lock_time)
    await facade.get_available_from_sql()
    await facade.prepare_proxies()
    return facade.result


# , response_model=S.PatchResponseAvailableProxy
@router.patch("")
async def change_proxy(data: S.PatchRequestAvailableProxy = Body()):
    if data.parsed_service is None:
        parsed_service = await R.ParsedService.get_name_by_id(data.parsed_service_id)
    else:
        parsed_service = data.parsed_service
    # Инициализирую Фасад
    facade = FacadeRotationPatch(
        **data.dump_to_putch_facade(),
        parsed_service=parsed_service
    )
    await facade.get_available_from_sql()

    # Смотрим прошлые баны
    last_blocks = await R.Error.get_last_hours(
        data.id,
        data.parsed_service_id,
        data.ignore_hours)

    # Логика блокировка прокси
    params = data.params if data.params else {}
    calculator = CalculateDelay(data.logic, last_blocks, params)
    delay = calculator.calculate_time()

    # Пишем ошибки в базы
    await R.ProxyBlocked.add(data.id, parsed_service, delay)
    await R.Error.add_one(**data.dump_to_sql_error(), sleep_time=delay)

    # Получаем новый прокси
    result = await facade.prepare_proxy()
    return result
