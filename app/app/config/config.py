from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from configparser import ConfigParser
from dotenv import load_dotenv
from typing import Literal
from app.utils.functions import get_env_prefix

load_dotenv()

CONFIG_PATH = "config.ini"

_config_ini = ConfigParser()
_config_ini.read(CONFIG_PATH)


class _Database(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=get_env_prefix("POSTGRES"), case_sensitive=False)
    engine: str = "+asyncpg"
    db: str
    password: str
    user: str
    host: str
    port: int

    @property
    def url(self):
        return f"postgresql{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def url_sync(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class _Logs(BaseModel):
    rotation: str = _config_ini.get('logs', 'rotation')
    level: str = _config_ini.get('logs', 'level')
    path: str = datetime.now().strftime('logs/%Y_%m_%d_log.log')


class _Settings(BaseSettings):
    MODE: Literal['DEV', "TEST", "PROD"] = 'DEV'
    db: _Database = _Database()
    logs: _Logs = _Logs()
    name: str = _config_ini.get('default', 'name')
    APIKEY: str


settings = _Settings()
