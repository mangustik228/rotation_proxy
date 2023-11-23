from fastapi import APIRouter, status, HTTPException
import app.repo as R
import app.schemas as S
from app.exceptions import DuplicateKey

router = APIRouter(prefix="/locations", tags=["LOCATION"])


@router.get("", response_model=S.GetResponseLocationList)
async def get_locations():
    result = await R.Location.get_all()
    return {"status": "success", "locations": result}


@router.get("/{id}", response_model=S.Location)
async def get_location(id: int):
    result = await R.Location.get_by_id(id)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("", response_model=S.PostResponseLocation, status_code=status.HTTP_201_CREATED)
async def post_location(data: S.PostRequestLocation):
    try:
        result = await R.Location.add_one(**data.model_dump())
        return {"status": "success", "location": result}
    except DuplicateKey:
        raise HTTPException(status.HTTP_409_CONFLICT, "name is already exist")


@router.put("/{id}", response_model=S.PutResponseLocation, status_code=status.HTTP_201_CREATED)
async def change_location(id: int, data: S.PutRequestLocation):
    try:
        result = await R.Location.update(id, **data.model_dump())
        if result:
            return {"status": "success", "location": result}
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
    except DuplicateKey as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
