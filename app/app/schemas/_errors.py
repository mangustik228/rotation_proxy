from typing import Literal
from pydantic import ConfigDict, BaseModel, Field


class BaseError(BaseModel):
    ...


class PostRequestError(BaseModel):
    reason: str
    proxy_id: int


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
