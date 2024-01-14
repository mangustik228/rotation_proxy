import asyncio
from collections import Counter

from fastapi import APIRouter, Query

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/stats", tags=["STATS"])


@router.get("/common",
            response_model=S.GetResponseStatsCommon
            )
async def get_base_stats():

    total_proxies = asyncio.create_task(R.Proxy.get_total_count())
    available_proxies = asyncio.create_task(R.Proxy.get_active_count())
    available_by_services = asyncio.create_task(
        R.Proxy.get_active_by_services())
    busies = asyncio.create_task(R.ProxyBusy.get_all())
    blocks = asyncio.create_task(R.ProxyBlocked.get_all())
    await asyncio.gather(total_proxies, available_proxies, available_by_services, busies, blocks)
    blocks_counter = Counter()
    for blocked in blocks.result():
        blocks_counter[blocked.split("_")[1]] += 1

    return {
        "total_proxies": total_proxies.result(),
        "available_proxies": available_proxies.result(),
        "busies": len(busies.result()),
        "available_by_services": available_by_services.result(),
        "blocks": blocks_counter
    }


@router.get("/expires",
            response_model=list[S.GetResponseStatsExpires])
async def get_stats_by_expire():
    stats_by_expire = await R.Proxy.get_stats_by_expire()
    return stats_by_expire


@router.get("/reasons")
async def get_group_errors_by_reason():
    stats = await R.Error.group_by_reasons()
    return stats


@router.get("/errors/{service}")
async def get_group_errors_by_service(service):
    service_id = await R.ParsedService.get_id_by_name(service)
    stats = await R.Error.get_group_errors_by_service(service_id)
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
