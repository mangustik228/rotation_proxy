from fastapi import APIRouter
import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/errors", tags=["ERRORS"])


@router.post("")
async def post_error(data: S.PostRequestError):
    result = await R.Error.add_one(**data.model_dump())
