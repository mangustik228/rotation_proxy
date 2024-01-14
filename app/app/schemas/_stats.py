from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GetResponseStatsByService(BaseModel):
    busies_all: int
    blocks_by_service: int
    errors_last_time: int
    errors_all_time: int
    last_error: datetime


class ServiceInfo(BaseModel):
    name: str
    count: int


class GetResponseStatsExpires(BaseModel):
    service: str
    count: int
    expire: datetime


class GetResponseStatsCommon(BaseModel):
    total_proxies: int
    available_proxies: int
    busies: int
    available_by_services: list[ServiceInfo]
    blocks: dict[str, int]
