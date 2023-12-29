import pytest
import logging
from loguru import logger


@pytest.fixture(scope="session", autouse=True)
def disallow_logging():
    logging.disable(logging.INFO)
    ...


@pytest.fixture(scope="session", autouse=True)
def disallow_loguru_logger():
    while True:
        try:
            logger.remove(0)
        except ValueError:
            break
