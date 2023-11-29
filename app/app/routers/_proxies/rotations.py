from fastapi import APIRouter, HTTPException, status
from app.db_redis import REDIS
import app.repo as R
import app.schemas as S
from app.exceptions import NotValidExpire
from app.utils.functions import get_valid_expire
import random
from app.services import FacadeRotation

router = APIRouter(prefix="/proxies/rotations", tags=["ROTATIONS"])


@router.get("")
async def get_available(
        parsing_service: str,
        count: int | None = 5,
        expire: str | None = None,
        location_id: int | None = 1,
        type_id: int | None = 1):
    try:
        expire = get_valid_expire(expire)
    except NotValidExpire as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))

    proxies_models = await R.Proxy.get_available(expire, location_id, type_id)
    FacadeRotation.shuffle_proxies(proxies_models)
    proxies = FacadeRotation.prepare_proxies(
        proxies_models,
        parsing_service,
        count
    )

    return proxies


@router.get("/set_value/{value}")
async def set_value(value: str):
    await REDIS.set("first_key", value, ex=10)
    return {"status": "ok"}


@router.get("/get_value/{value}")
async def get_value():
    value = await REDIS.get("first_key")
    return {"value": value}
