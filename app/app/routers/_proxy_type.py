from fastapi import APIRouter, Body, HTTPException, status

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/types", tags=["TYPES"])


@router.get("",
            response_model=S.GetRequestProxyTypeList,
            description="Посмотреть доступные типы прокси")
async def get_types():
    result = await R.ProxyType.get_all()
    return {"status": "success", "types": result}


@router.get("/name/{name}",
            response_model=S.GetResponseProxyTypeByName,
            description="Получить прокси по имени",)
async def get_proxy_type_by_name(name: str):
    result = await R.ProxyType.get_id_by_name(name)
    if result:
        return {"status": "exist", "id": result}
    raise HTTPException(404, "Not found")


@router.get("/{id}",
            response_model=S.ProxyType,
            description="Посмотреть тип прокси по id")
async def get_type(id: int):
    result = await R.ProxyType.get_by_id(id)
    if result:
        return result
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("",
             response_model=S.PostResponseProxyType,
             status_code=status.HTTP_201_CREATED,
             description="Добавить тип прокси")
async def post_proxy_type(data: S.PostRequestProxyType = Body()):
    result = await R.ProxyType.add_one(**data.model_dump())
    return {"status": "created", "type": result}


@router.put("/{id}",
            response_model=S.PutResponseProxyType,
            status_code=status.HTTP_201_CREATED,
            description="Изменить тип прокси")
async def change_proxy(id: int, data: S.PutRequestProxyType):
    result = await R.ProxyType.update(id, **data.model_dump())
    if result:
        return {"status": "updated", "type": result}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
