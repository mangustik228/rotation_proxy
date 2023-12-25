from datetime import datetime
from typing import Literal
from pydantic import ConfigDict, BaseModel, Field
from ._proxies import ProxyLight


class BaseError(BaseModel):
    id: int
    created_at: datetime
    proxy_id: int
    reason: str
    parsed_service: str


class PostRequestError(BaseModel):
    reason: str
    proxy_id: int = Field(gt=0)
    parsed_service_id: int


class PostResponseError(BaseModel):
    status: str
    error_id: int


class GetResponseErrorList(BaseModel):
    status: Literal["ok"]
    count: int
    proxy: ProxyLight
    errors: list[BaseError]
