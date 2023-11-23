from datetime import datetime, date
import re
from pydantic import BaseModel, field_validator


class ProxyBase(BaseModel):
    server: str
    username: str
    password: str
    port: int
    expire: date | datetime
    service_id: int | None
    location_id: int | None = 1
    type_id: int | None = 1

    @field_validator('server')
    def valid_server(cls, v):
        try:
            return re.findall(r'\d+\.\d+\.\d+\.\d+', v)[0]
        except:
            raise ValueError(f'Uncorrect field "server": {v}')
