from typing import Literal
from typing import Literal
from pydantic import BaseModel, ConfigDict


class AvailableProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    server: str
    port: int
    username: str
    password: str

    def __str__(self, parsing_service):
        return f'{parsing_service}_{self.id}'


class GetResponseAvailableProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["full", "not full"]
    data: list[AvailableProxy]


class PatchRequestAvailableProxy(BaseModel):
    id: int
    service: str
    reason: str
    logic: Literal["base", "geometry"] = "base"
    expire_proxy: str | None = None
    location_id: int = 1
    type_id: int = 1
    lock_time: int = 300


class PatchResponseAvailableProxy(AvailableProxy):
    ...
