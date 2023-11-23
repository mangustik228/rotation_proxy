from fastapi import APIRouter


router = APIRouter(prefix="/locations")


@router.get("")
async def get_location():
    ...
