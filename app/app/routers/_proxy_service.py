from fastapi import APIRouter, Body, HTTPException, status

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/services",
                   tags=["SERVICES"])


@router.get("", response_model=S.GetResponseProxyServiceList)
async def get_services():
    # R.ProxyService.
    result = await R.ProxyService.get_all()
    return {"services": result}


@router.get("/{id}", response_model=S.ProxyService)
async def get_service(id: int):
    result = await R.ProxyService.get_by_id(id)
    if result:
        return result
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("",
             status_code=status.HTTP_201_CREATED)
async def post_service(data: S.PostRequestProxyService = Body()):
    result = await R.ProxyService.add_one(**data.model_dump())
    return {"status": "created",
            "service": result}


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED)
async def change_service_name(id: int, data: S.PutRequestProxyService = Body()):
    result = await R.ProxyService.update(id, **data.model_dump())
    if result:
        return {"status": "updated", "service": result}
    raise HTTPException(status.HTTP_404_NOT_FOUND)
