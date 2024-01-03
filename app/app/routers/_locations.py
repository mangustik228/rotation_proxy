from fastapi import APIRouter, HTTPException, status

import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/locations", tags=["LOCATION"])


@router.get("",
            response_model=S.GetResponseLocationList,
            description="Получить список всех доступных геолокаций")
async def get_locations():
    result = await R.Location.get_all()
    return {"status": "success", "locations": result}


@router.get("/{id}",
            response_model=S.Location,
            description="Получить геолокацию по id")
async def get_location(id: int):
    result = await R.Location.get_by_id(id)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("",
             response_model=S.PostResponseLocation,
             status_code=status.HTTP_201_CREATED,
             description="Добавить геолокацию")
async def post_location(data: S.PostRequestLocation):
    result = await R.Location.add_one(**data.model_dump())
    return {"status": "created", "location": result}


@router.put("/{id}",
            response_model=S.PutResponseLocation,
            status_code=status.HTTP_201_CREATED,
            description="Изменить геолокацию")
async def change_location(id: int, data: S.PutRequestLocation):
    result = await R.Location.update(id, **data.model_dump())
    if result:
        return {"status": "updated", "location": result}
    raise HTTPException(status.HTTP_404_NOT_FOUND)
