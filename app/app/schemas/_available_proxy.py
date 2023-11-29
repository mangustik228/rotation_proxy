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


class ResponseAvailableProxy(AvailableProxy):
    uuid: str = Field(default_factory=uuid.uuid4)
    parsing_service: str
