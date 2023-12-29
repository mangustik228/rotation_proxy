import os

from alembic import command
from alembic.config import Config


async def update_db():
    assert os.getenv("MODE") == "TEST", "base is not test"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_section_option("logger_alembic", "level", "WARN")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
