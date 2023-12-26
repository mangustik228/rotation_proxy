from typing import Any, Literal
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
    parsed_service_id: int
    ignore_blocks_older_then_hours: int = 24
    parsed_service: str | None = None
    expire_proxy: str | None = None
    location_id: int = 1
    type_id: int = 1
    lock_time: int = 300
    reason: str
    params: dict[str, Any] | None = None
    logic: Literal["base", "geometry"] = "base"

    def dump_to_facade(self):
        return {
            "expire_proxy": self.expire_proxy,
            "location_id": self.location_id,
            "type_id": self.type_id,
            "count": 1,
            "lock_time": self.lock_time,
        }


class PatchResponseAvailableProxy(AvailableProxy):
    ...
