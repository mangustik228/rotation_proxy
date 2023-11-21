import sys
from loguru import logger
from app.config import settings
import os
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class ConfigLogging:
    @classmethod
    def setup(cls):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        if settings.MODE != "TEST":
            # logger.remove(0)
            # cls._add_serialized_logger()
            ...
        if settings.MODE == "PROD":
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
            retention=settings.logs.retention,
            serialize=True)
