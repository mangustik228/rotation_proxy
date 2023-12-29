from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator


class ParsedServiceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class PostRequestParsedService(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name(cls, v):
        if "_" in v:
            raise ValidationError("name cannot contain symbol `_`")
        return v


class PostResponseParsedService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["created"]
    parsed_service: ParsedServiceBase


class GetResponseParsedServiceList(BaseModel):
    status: Literal["success"]
    count: int
    parsed_services: list[ParsedServiceBase]


class PutRequestParsedService(BaseModel):
    name: str


class PutResponseParsedService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["updated"]
    parsed_service: ParsedServiceBase


class GetResponseParsedServiceByName(BaseModel):
    status: Literal["exist"]
    id: int
