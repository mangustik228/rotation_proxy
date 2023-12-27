from fastapi import APIRouter
import app.schemas as S
import app.repo as R

router = APIRouter(prefix="/proxies/blocks")


@router.get("", response_model=list[S.GetResponseBlockProxy])
async def get_busies_proxy():
    data = await R.ProxyBlocked.get_all_with_expire()
    return data
