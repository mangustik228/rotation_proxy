from fastapi import APIRouter, Body, HTTPException, status

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/parsed_services", tags=["PARSED_SERVICES"])


@router.get("/name/{name}",
            response_model=S.GetResponseParsedServiceByName,
            description="Получить id парсящегося сервиса по его имени.")
async def get_parsed_service_by_name(name: str):
    result = await R.ParsedService.get_id_by_name(name)
    if result:
        return {
            "status": "exist",
            "id": result}
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.get("/id/{id}",
            response_model=S.ParsedServiceBase,
            description="Получить имя парсящегося сервиса по id")
async def get_parsed_service_by_id(id: int):
    result = await R.ParsedService.get_by_id(id)
    if result:
        return result
    raise HTTPException(status.HTTP_404_NOT_FOUND, "not founded")


@router.get("",
            response_model=S.GetResponseParsedServiceList,
            description="Получить список всех парсящихся сервисов")
async def get_parsed_services():
    result = await R.ParsedService.get_all()
    return {
        "status": "success",
        "count": len(result),
        "parsed_services": result
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_parsed_service(data: S.PostRequestParsedService = Body()):
    result = await R.ParsedService.add_one(**data.model_dump())
    return {"status": "created", "parsed_service": result}


@router.put("/{id}",
            response_model=S.PutResponseParsedService,
            status_code=status.HTTP_201_CREATED)
async def update_proxy_name(id: int, data: S.PutRequestParsedService):
    result = await R.ParsedService.update(id, **data.model_dump())
    if result:
        return {"status": "updated", "parsed_service": result}
    raise HTTPException(status.HTTP_404_NOT_FOUND)
