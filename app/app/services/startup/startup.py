import app.repo as R
from loguru import logger
from .config_logger import ConfigLogging


async def prepare_db():
    ConfigLogging.setup()
    logger.info("application is started")
