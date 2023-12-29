from datetime import datetime

from pydantic import BaseModel


class ValidateDate(BaseModel):
    date: datetime
