from fastapi import APIRouter, HTTPException, status

import app.repo as R
import app.schemas as S
from app.services import transform_data_from_orm_dict

router = APIRouter(prefix="/errors", tags=["ERRORS"])


@router.get("/proxy/{id}",
            description="Получить ошибки для определенной прокси")
async def get_errors_by_proxy(id: int) -> S.GetResponseErrorByProxy:
    proxy = await R.Proxy.get_by_id(id)
    if proxy is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Proxy not found")
    errors = await R.Error.get_by_proxy_id(id)
    if len(errors) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not errors")
    return {
        "status": "success",
        "count": len(errors),
        "proxy": proxy,
        "errors": errors
    }


@router.get("/group_by_services")
async def group_by_services():
    errors = await R.Error.get_stats_by_services()
    return transform_data_from_orm_dict(errors)


@router.get("/parsed_service/{id}",
            response_model=S.GetResponseErrorByParsedService,
            description="Получить ошибки по определенному сервису")
async def get_errors_by_parsed_service(id: int):
    service = await R.ParsedService.get_by_id(id)
    if service is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    errors = await R.Error.get_by_service_id(id)
    if len(errors) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not errors")
    return {
        "status": "success",
        "count": len(errors),
        "parsed_service": service,
        "errors": errors
    }


@router.post("",
             response_model=S.PostResponseError,
             status_code=status.HTTP_201_CREATED,
             description="Опубликовать ошибку. Ручка тестовая. просьба не пользоваться")
async def post_error(data: S.PostRequestError):
    result = await R.Error.add_one(**data.model_dump())
    if result is not None:
        return {
            "status": "created",
            "error_id": result.id
        }
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail="probably not found proxy_id")
