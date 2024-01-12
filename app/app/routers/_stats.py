import asyncio

from fastapi import APIRouter, Query

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/stats", tags=["STATS"])


@router.get("/reasons")
async def get_group_errors_by_reason():
    stats = await R.Error.group_by_reasons()
    return stats


@router.get("/{service}",
            response_model=S.GetResponseStatsByService,
            summary="Получить статистику по запросам прокси определенного parsed_servcie")
async def get_stats_by_service(service: str, hours: int = 24):
    busies = asyncio.create_task(R.ProxyBusy.get_all())
    blocks = asyncio.create_task(R.ProxyBlocked.get_all_by_service(service))
    service_id = asyncio.create_task(R.ParsedService.get_id_by_name(service))
    await asyncio.gather(busies, blocks, service_id)

    errors_last_time = asyncio.create_task(
        R.Error.get_count_by_service_id_last_time(service_id.result(), hours))
    errors_all_time = asyncio.create_task(
        R.Error.get_count_errors_by_service(service_id.result()))
    last_error = asyncio.create_task(
        R.Error.get_time_last_error(service_id.result())
    )
    await asyncio.gather(errors_last_time, errors_all_time, last_error)

    return {
        "busies_all": len(busies.result()),
        "blocks_by_service": len(blocks.result()),
        "errors_last_time": errors_last_time.result(),
        "errors_all_time": errors_all_time.result(),
        "last_error": last_error.result()
    }


@router.get("/errors/{service}")
async def get_group_errors_by_service(service):
    service_id = await R.ParsedService.get_id_by_name(service)
    stats = await R.Error.get_group_errors_by_service(service_id)
    return stats
