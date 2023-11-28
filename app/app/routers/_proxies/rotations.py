from fastapi import APIRouter
from app.db_redis import REDIS

router = APIRouter(prefix="/proxies/rotations", tags=["ROTATIONS"])


@router.get("")
def foo():
    return "success"


@router.get("/set_value/{value}")
async def set_value(value: str):
    await REDIS.set("first_key", value, ex=10)
    return {"status": "ok"}


@router.get("/get_value/{value}")
async def get_value():
    value = await REDIS.get("first_key")
    return {"value": value}
