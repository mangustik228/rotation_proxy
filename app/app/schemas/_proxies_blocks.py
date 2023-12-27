from pydantic import BaseModel


class GetResponseBlockProxy(BaseModel):
    id: int
    expire: int
    service: str
