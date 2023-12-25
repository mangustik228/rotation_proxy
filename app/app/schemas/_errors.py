from datetime import datetime
from typing import Literal
from pydantic import ConfigDict, BaseModel, Field
from ._proxies import ProxyLight


class BaseError(BaseModel):
    id: int
    created_at: datetime
    proxy_id: int
    reason: str


class PostRequestError(BaseModel):
    reason: str
    proxy_id: int = Field(gt=0)


class PostResponseError(BaseModel):
    status: str
    error_id: int


class GetResponseErrorList(BaseModel):
    status: Literal["ok"]
    count: int
    proxy: ProxyLight
    errors: list[BaseError]


# class ProxyType(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
#     name: str


# class GetRequestProxyTypeList(BaseModel):
#     types: list[ProxyType]


# class GetRequestProxyType(ProxyType):
#     ...


# class PostRequestProxyType(BaseModel):
#     name: str


# class PostResponseProxyType(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     status: Literal["created"]
#     proxy_type: ProxyType = Field(alias="type")


# class PutRequestProxyType(BaseModel):
#     name: str


# class PutResponseProxyType(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     status: Literal["updated"]
#     proxy_type: ProxyType = Field(alias="type")
