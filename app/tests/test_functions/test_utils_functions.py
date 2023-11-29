from app.utils.functions import get_valid_expire
import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from app.exceptions import NotValidExpire


@pytest.mark.parametrize(
    "expire, result",
    [
        (None, datetime(2023, 11, 30, 12, 0, 0)),
        ("2023-12-01T13:00:00", datetime(2023, 12, 1, 13, 0, 0))
    ]
)
@freeze_time("2023-11-29 12:00:00")
def test_get_valid_expire(expire, result):
    date = get_valid_expire(expire)
    assert date == result


def test_get_valid_expire_error():
    with pytest.raises(NotValidExpire):
        get_valid_expire("2023-11-29")
