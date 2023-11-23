from fastapi import APIRouter


router = APIRouter(prefix="/types")


@router.get("")
async def get_types():
    ...
