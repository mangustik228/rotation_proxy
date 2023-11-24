from typing import Literal
from pydantic import ConfigDict, BaseModel, Field


class ProxyType(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class GetRequestProxyTypeList(BaseModel):
    types: list[ProxyType]


class GetRequestProxyType(ProxyType):
    ...


class PostRequestProxyType(BaseModel):
    name: str


class PostResponseProxyType(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["success"]
    proxy_type: ProxyType = Field(alias="type")


class PutRequestProxyType(BaseModel):
    name: str


class PutResponseProxyType(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["success"]
    proxy_type: ProxyType = Field(alias="type")
