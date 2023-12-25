from fastapi import APIRouter, HTTPException, status, Body
import app.repo as R
import app.schemas as S
from app.exceptions import DuplicateKey

router = APIRouter(prefix="/parsed_services", tags=["PARSED_SERVICES"])


@router.get("", response_model=S.GetResponseParsedServiceList)
async def get_parsed_services():
    result = await R.ParsedService.get_all()
    return {
        "status": "success",
        "count": len(result),
        "parsed_services": result
    }


@router.get("/{id}", response_model=S.ParsedServiceBase)
async def get_parsed_service_by_id(id: int):
    result = await R.ParsedService.get_by_id(id)
    if result:
        return result
    raise HTTPException(status.HTTP_404_NOT_FOUND, "not founded")


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_parsed_service(data: S.PostRequestParsedService = Body()):
    try:
        result = await R.ParsedService.add_one(**data.model_dump())
        return {"status": "created", "parsed_service": result}
    except DuplicateKey:
        raise HTTPException(status.HTTP_409_CONFLICT, "name is already exist")


@router.put("/{id}",
            response_model=S.PutResponseParsedService,
            status_code=status.HTTP_201_CREATED)
async def update_proxy_name(id: int, data: S.PutRequestParsedService):
    try:
        result = await R.ParsedService.update(id, **data.model_dump())
        if result:
            return {"status": "updated", "parsed_service": result}
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except DuplicateKey as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
