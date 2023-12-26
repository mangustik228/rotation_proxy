from datetime import datetime
from typing import Literal
from pydantic import ConfigDict, BaseModel, Field
from ._proxies import ProxyLight
from ._parsed_services import ParsedServiceBase


class BaseError(BaseModel):
    id: int
    created_at: datetime
    proxy_id: int
    reason: str
    parsed_service_id: int
    sleep_time: int


class PostRequestError(BaseModel):
    reason: str
    proxy_id: int = Field(gt=0)
    parsed_service_id: int
    sleep_time: int


class PostResponseError(BaseModel):
    status: Literal["created"]
    error_id: int


class GetResponseErrorByProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["success"]
    count: int
    proxy: ProxyLight
    errors: list[BaseError]


class GetResponseErrorByParsedService(BaseModel):
    status: Literal["success"]
    count: int
    parsed_service: ParsedServiceBase
    errors: list[BaseError]
