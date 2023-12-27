from pydantic import BaseModel


class GetResponseBusyProxy(BaseModel):
    id: int
    expire: int
