from unittest.mock import patch

import pytest

from app.middlewares.log_middleware import LogMiddleware


async def mock_middleware_dispatch(self, request, call_next):
    return await call_next(request)


@pytest.fixture(autouse=True)
def mock_method_to_mock():
    with patch.object(LogMiddleware, "dispatch", new=mock_middleware_dispatch) as mock_method:
        yield
