import os
from datetime import datetime, timedelta
from pydantic import ValidationError
from app.exceptions import NotValidExpire
import app.schemas as S


def get_env_prefix(variable: str):
    if os.getenv("MODE") == "DEV":
        return f"DEV_{variable}_"
    elif os.getenv("MODE") == "TEST":
        return f"TEST_{variable}_"
    elif os.getenv("MODE") == "PROD":
        return f"{variable}_"
    else:
        raise ValueError("MODE must be DEV / TEST / PROD")


def get_valid_expire(expire: str | None) -> datetime:
    if expire is None:
        return datetime.now().replace(second=0, microsecond=0) + timedelta(days=1)
    try:
        return S.ValidateDate(date=expire).date
    except ValidationError:
        raise NotValidExpire(
            "expire must be format '2023-12-01T00:00:00` or None")
