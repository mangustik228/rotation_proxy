from datetime import datetime, date
import re
from typing import Literal
from pydantic import BaseModel, field_validator, ConfigDict, Field
from ._proxy_services import ProxyService
from ._proxy_types import ProxyType
from ._locations import Location


class Proxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    server: str
    username: str
    password: str
    port: int
    expire: datetime


class ProxyLight(Proxy):
    service_id: int
    type_id: int
    location_id: int


class PostResponseProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["created"]
    proxy: Proxy


class GetResponseProxy(Proxy):
    service: ProxyService
    proxy_type: ProxyType
    location: Location


class GetResponseProxyList(BaseModel):
    total_count: int
    total_active_count: int
    status: Literal["success"]
    proxies: list[GetResponseProxy]


class PostResponseProxyList(BaseModel):
    status: Literal["created"]
    count_added: int
    count_errors: int


class PostRequestProxy(BaseModel):
    server: str
    username: str
    password: str
    port: int
    expire: datetime
    location_id: int = Field(gt=0)
    type_id: int = Field(gt=0)
    service_id: int = Field(gt=0)

    @field_validator('server')
    def valid_server(cls, v):
        try:
            return re.findall(r'\d+\.\d+\.\d+\.\d+', v)[0]
        except:
            raise ValueError(f'Uncorrect field "server": {v}')


class PutRequestProxy(PostRequestProxy):
    ...


class PutResponseProxy(BaseModel):
    status: Literal["updated"]
    proxy: ProxyLight


class PatchRequestProxy(BaseModel):
    server: str | None = None
    username: str | None = None
    password: str | None = None
    port: int | None = None
    expire: datetime | None = None
    service_id: int | None = None
    type_id: int | None = None
    location_id: int | None = None


class PatchResponseProxy(BaseModel):
    status: Literal["updated"]
    proxy: ProxyLight
