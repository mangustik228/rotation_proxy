from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class AvailableProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    server: str
    port: int
    username: str
    password: str

    def __str__(self, parsing_service):
        return f'{parsing_service}_{self.id}'


class GetResponseOneProxy(AvailableProxy):
    ...


class GetRequestOneProxy(BaseModel):
    parsed_service_id: int
    parsed_service: str | None = None
    location_id: int | None = None
    expire_proxy: str | None = None
    type_id: int = 1
    lock_time: int = 300


class GetResponseFreeProxy(BaseModel):
    status: Literal["success",
                    "proxies doesn't found"] = Field(..., description="just description")


class GetRequestAvailableProxy(BaseModel):
    parsed_service_id: int
    parsed_service: str | None = None
    count: int = 5
    location_id: int | None = None
    type_id: int | None = 1
    lock_time: int | None = 300
    expire_proxy: str | None = None


class GetResponseAvailableProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["full", "not full"]
    data: list[AvailableProxy]


class PutRequestAvailableProxy(BaseModel):
    id: int = Field(alias="proxy_id")
    parsed_service_id: int
    parsed_service: str | None = None
    location_id: int | None = None
    expire_proxy: str | None = None
    type_id: int = 1
    lock_time: int = 300


class PatchRequestAvailableProxy(BaseModel):
    id: int = Field(alias="proxy_id")
    parsed_service_id: int
    parsed_service: str | None = None
    expire_proxy: str | None = None
    location_id: int | None = None
    type_id: int = 1
    lock_time: int = 300
    reason: str | int
    params: dict[str, Any] | None = None
    logic: Literal["sum_history", "linear"] = "linear"
    ignore_hours: int = 24

    def dump_to_get_facade(self):
        return {
            "expire_proxy": self.expire_proxy,
            "location_id": self.location_id,
            "type_id": self.type_id,
            "count": 1,
            "lock_time": self.lock_time,
        }

    def dump_to_putch_facade(self):
        return {
            "id": self.id,
            "parsed_service_id": self.parsed_service_id,
            "ignore_hours": self.ignore_hours,
            "expire_proxy": self.expire_proxy,
            "location_id": self.location_id,
            "type_id": self.type_id,
            "lock_time": self.lock_time,
            "reason": self.reason,
            "params": self.params,
            "logic": self.logic
        }

    def dump_to_sql_error(self):
        return {
            "proxy_id": self.id,
            "reason": str(self.reason),
            "parsed_service_id": self.parsed_service_id
        }


class PatchResponseAvailableProxy(AvailableProxy):
    ...
