from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GetResponseStatsByService(BaseModel):
    busies_all: int
    blocks_by_service: int
    errors_last_time: int
    errors_all_time: int
    last_error: datetime
