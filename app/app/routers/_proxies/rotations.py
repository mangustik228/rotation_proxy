from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException
from loguru import logger

import app.repo as R
import app.schemas as S
from app.docs.rotation import (DESCRIPTION_CHANGE_WITHOUT_ERROR,
                               DESCRIPTION_FREE_PROXY,
                               DESCRIPTION_GET_AVAILABLE,
                               DESCRIPTION_PATCH_PROXY,
                               DESCRIPTION_ONE_PROXY)
from app.services import (CalculateDelay, FacadeRotationAvailable,
                          FacadeRotationPatch, FacadeSimpleChange)

router = APIRouter(prefix="/proxies/rotations", tags=["ROTATIONS"])


@router.get("/free/{id}",
            response_model=S.GetResponseFreeProxy,
            description=DESCRIPTION_FREE_PROXY)
async def free_proxy(id: int):
    if await R.ProxyBusy.get(id):
        await R.ProxyBusy.free(id)
        return {"status": "success"}
    return {"status": "proxies doesn't found"}


@router.get("/one",
            response_model=S.GetResponseOneProxy,
            description=DESCRIPTION_ONE_PROXY)
async def get_one_proxy(params: S.GetRequestOneProxy = Depends()):
    if (parsed_service := params.parsed_service) is None:
        parsed_service = await R.ParsedService.get_name_by_id(params.parsed_service_id)
    facade = FacadeSimpleChange(
        **params.model_dump(exclude=["parsed_service_id", "parsed_service"]), parsed_service=parsed_service)

    await facade.get_available_from_sql()
    logger.info(f"available_proxies = {len(facade.proxies_models)}")
    new_proxy = await facade.get_free_proxy()
    return new_proxy


@router.get("",
            response_model=S.GetResponseAvailableProxy,
            description=DESCRIPTION_GET_AVAILABLE)
async def get_available(params: S.GetRequestAvailableProxy = Depends()):
    if (parsed_service := params.parsed_service) is None:
        parsed_service = await R.ParsedService.get_name_by_id(params.parsed_service_id)

    facade = FacadeRotationAvailable(
        **params.model_dump(exclude=["parsed_service", "parsed_service_id"]),
        parsed_service=parsed_service)

    await facade.get_available_from_sql()
    logger.info(f"available_proxies = {len(facade.proxies_models)}")
    await facade.prepare_proxies()
    return facade.result


@router.put("",
            description=DESCRIPTION_CHANGE_WITHOUT_ERROR,
            response_model=S.AvailableProxy)
async def change_proxy_without_error(data: S.PutRequestAvailableProxy):
    if (parsed_service := data.parsed_service) is None:
        parsed_service = await R.ParsedService.get_name_by_id(data.parsed_service_id)
    facade = FacadeSimpleChange(
        **data.model_dump(exclude=["id", "parsed_service", "parsed_service_id"]),
        parsed_service=parsed_service)
    await facade.get_available_from_sql()
    new_proxy = await facade.get_free_proxy()
    await facade.free_old_proxy(data.id)
    return new_proxy


@router.patch("",
              description=DESCRIPTION_PATCH_PROXY,
              response_model=S.PatchResponseAvailableProxy)
async def change_proxy_with_error(data: S.PatchRequestAvailableProxy = Body()):
    if (parsed_service := data.parsed_service) is None:
        parsed_service = await R.ParsedService.get_name_by_id(data.parsed_service_id)

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

    # Пишем ошибки в базы и освобождаем
    await R.ProxyBlocked.add(data.id, parsed_service, delay)
    await R.ProxyBusy.free(data.id)
    await R.Error.add_one(**data.dump_to_sql_error(), sleep_time=delay)

    # Получаем новый прокси
    result = await facade.prepare_proxy()
    return result
