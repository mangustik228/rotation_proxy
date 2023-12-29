import os
import sys

from loguru import logger

from app.config import settings


class ConfigLogging:
    @classmethod
    def setup(cls):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        if settings.MODE == "PROD" or settings.MODE == "DEV":
            cls._add_file_logger()

    @classmethod
    def _add_serialized_logger(cls):
        logger.add(
            sink=sys.stdout,
            level="TRACE",
            serialize=True,
        )

    @classmethod
    def _add_file_logger(cls):
        logger.add(
            sink="logs/{time:YYYY-MM-DD}.log",
            rotation=settings.logs.rotation,
            level=settings.logs.level,
            serialize=True)
