from typing import Literal

from pydantic import BaseModel, ConfigDict


class ProxyService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None


class GetResponseProxyServiceList(BaseModel):
    services: list[ProxyService]


class PostRequestProxyService(BaseModel):
    name: str


class PostResponseProxyService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["created"]
    service: ProxyService


class PutRequestProxyService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class PutResponseProxyService(BaseModel):
    status: Literal["updated"]
    service: ProxyService
