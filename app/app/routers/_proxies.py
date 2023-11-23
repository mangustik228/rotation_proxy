from datetime import datetime
from fastapi import HTTPException
from fastapi import APIRouter, status, Body
import app.schemas as S
import app.repo as R
from app.services import ProxyFormater
from app.exceptions import DuplicateKey

router = APIRouter(prefix="/proxies", tags=["PROXIES"])


@router.get("")
async def get_proxies(service: str | None = None,
                      location_id: int | None = 1,
                      count: int = 25,
                      format: str = "short",
                      app_type: str = "playwright",
                      expire: datetime = datetime.utcnow(),
                      type_id: int | None = 1):
    '''
    Get current proxies:   
    **format:** Literal["full", "queue", "short"]
      - full
        ```python 
        [{
            "server": "...", 
            "username": "...", 
            "password"" "..." 
        }]
        ```
    **app_type:** Literal["requests", "playwright"] 

    '''
    result = await R.Proxy.get_all(count)
    try:
        return ProxyFormater.prepare_proxies(result, format, app_type)
    except ValueError as e:
        return HTTPException(422, str(e))


@router.get("/{id}")
async def get_proxy(id: int):
    ...


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proxy(id: int):
    ...


@router.post("/change")
async def change_proxy(data: S.ProxyBase = Body()):
    ...


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_proxies(data: list[S.ProxyBase] = Body()):
    try:
        await R.Proxy.add_many(data)
        return {"status": "ok"}
    except DuplicateKey as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e))


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_proxy(id: int):
    ...
