from typing import Literal

from pydantic import BaseModel, ConfigDict


class Location(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    parent_id: int | None


class GetResponseLocationByName(BaseModel):
    status: Literal["exist"]
    id: int


class GetResponseLocationList(BaseModel):
    status: Literal["success"]
    locations: list["Location"]


class GetResponseLocation(Location):
    ...


class PostRequestLocation(BaseModel):
    name: str


class PostResponseLocation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["created"]
    location: Location


class PutRequestLocation(BaseModel):
    name: str


class PutResponseLocation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["updated"]
    location: Location
