from pydantic import BaseModel, validator
from datetime import datetime, timedelta, date


class ValidateDate(BaseModel):
    date: datetime
