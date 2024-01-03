from fastapi import APIRouter

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/proxies/busies", tags=["PROXIES"])


@router.get("",
            response_model=list[S.GetResponseBusyProxy],
            description="Получить занятые прокси")
async def get_busies_proxy():
    data = await R.ProxyBusy.get_all_with_expire()
    return data
