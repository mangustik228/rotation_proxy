from fastapi import APIRouter, HTTPException, status, Body
import app.repo as R
import app.schemas as S
from app.exceptions import DuplicateKey

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
    try:
        result = await R.ProxyService.add_one(**data.model_dump())
    except DuplicateKey as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return {"status": "success",
            "service": result}


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def change_service_name(id: int, data: S.PutRequestProxyService = Body()):
    result = await R.ProxyService.update(id, **data.model_dump())
    if result:
        return {"status": "success", "service": result}
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
