from fastapi import APIRouter
import app.schemas as S
import app.repo as R

router = APIRouter(prefix="/proxies/busies")


@router.get("", response_model=list[S.GetResponseBusyProxy])
async def get_busies_proxy():
    data = await R.ProxyBusy.get_all_with_expire()
    return data
