from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
import uuid


class AvailableProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    server: str
    port: int
    username: str
    password: str

    def view(self, parsing_service):
        return f'{parsing_service}_{self.id}'


class GetResponseAvailableProxy(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: Literal["full", "not full"]
    data: list[AvailableProxy]
