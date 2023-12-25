from fastapi import APIRouter, HTTPException, status
import app.repo as R
import app.schemas as S

router = APIRouter(prefix="/errors", tags=["ERRORS"])


@router.post("", response_model=S.PostResponseError)
async def post_error(data: S.PostRequestError):
    result = await R.Error.add_one(**data.model_dump())
    if result is not None:
        return {
            "status": "created",
            "error_id": result.id}
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail="probably not found proxy_id")


@router.get("/proxy/{id}")
async def get_errors_by_id(id: int) -> S.GetResponseErrorList:
    proxy = await R.Proxy.get_by_id(id)
    if proxy is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not current proxy")
    errors = await R.Error.get_by_proxy_id(id)
    if len(errors) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not errors")
    return {
        "status": "ok",
        "count": len(errors),
        "proxy": proxy,
        "errors": errors
    }
    ...  # TODO Сделать занесение ошибок.
