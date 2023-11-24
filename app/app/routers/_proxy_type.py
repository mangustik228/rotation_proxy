from fastapi import APIRouter, HTTPException, status, Body
import app.repo as R
import app.schemas as S
from app.exceptions import DuplicateKey


router = APIRouter(prefix="/types", tags=["TYPES"])


@router.get("", response_model=S.GetRequestProxyTypeList)
async def get_types():
    result = await R.ProxyType.get_all()
    return {"status": "success", "types": result}


@router.get("/{id}", response_model=S.ProxyType)
async def get_type(id: int):
    result = await R.ProxyType.get_by_id(id)
    if result:
        return result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("", response_model=S.PostResponseProxyType, status_code=status.HTTP_201_CREATED)
async def post_proxy_type(data: S.PostRequestProxyType = Body()):
    try:
        result = await R.ProxyType.add_one(**data.model_dump())
        return {"status": "success", "type": result}
    except DuplicateKey:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail="item is already exist")


@router.put("/{id}", response_model=S.PostResponseProxyType, status_code=status.HTTP_201_CREATED)
async def change_proxy(id: int, data: S.PutRequestProxyType):
    try:
        result = await R.ProxyType.update(id, **data.model_dump())
        if result:
            return {"status": "success", "type": result}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except DuplicateKey:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
