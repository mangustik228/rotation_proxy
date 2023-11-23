from typing import Literal
from pydantic import ConfigDict, BaseModel


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
    name: str
    status: Literal["success"]
    _type: ProxyType


class PutRequestProxyType(BaseModel):
    id: int


class PutResponseProxyType(BaseModel):
    status: Literal["success"]
    _type: ProxyType
