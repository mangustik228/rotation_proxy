from fastapi import APIRouter

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/proxies/blocks", tags=["PROXIES"])


@router.get("",
            response_model=list[S.GetResponseBlockProxy],
            description="Получить заблокированные прокси")
async def get_busies_proxy():
    data = await R.ProxyBlocked.get_all_with_expire()
    return data
