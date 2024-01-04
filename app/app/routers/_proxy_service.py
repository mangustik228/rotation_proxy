from fastapi import APIRouter, Body, HTTPException, status

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/services",
                   tags=["SERVICES"])


@router.get("",
            response_model=S.GetResponseProxyServiceList,
            description="Получить список всех сервисов, предоставляющих прокси")
async def get_services():
    # R.ProxyService.
    result = await R.ProxyService.get_all()
    return {"services": result}


@router.get("/name/{name}",
            response_model=S.GetResponseProxyServiceByName,
            description="Получить прокси по имени",)
async def get_service_by_name(name: str):
    result = await R.ProxyService.get_id_by_name(name)
    if result:
        return {"status": "exist", "id": result}
    raise HTTPException(404, "Not found")


@router.get("/{id}",
            response_model=S.ProxyService,
            description="Получить сервис, предоставляющий прокси по id")
async def get_service(id: int):
    result = await R.ProxyService.get_by_id(id)
    if result:
        return result
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("",
             status_code=status.HTTP_201_CREATED,
             description="Опубликовать сервис, предоставляющий прокси")
async def post_service(data: S.PostRequestProxyService = Body()):
    result = await R.ProxyService.add_one(**data.model_dump())
    return {"status": "created",
            "service": result}


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED,
            description="Изменить сервис, предоставляющий прокси")
async def change_service_name(id: int, data: S.PutRequestProxyService = Body()):
    result = await R.ProxyService.update(id, **data.model_dump())
    if result:
        return {"status": "updated", "service": result}
    raise HTTPException(status.HTTP_404_NOT_FOUND)
