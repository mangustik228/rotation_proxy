from configparser import ConfigParser
from datetime import datetime
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

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


class BaseProxyService(BaseSettings):
    api_key: str
    url: str


class _ProxyIo(BaseProxyService):
    model_config = SettingsConfigDict(
        env_prefix="PROXY_IO_")


class _SpaceProxy(BaseProxyService):
    model_config = SettingsConfigDict(
        env_prefix="SPACEPROXY_")


class _ProxyNet(BaseProxyService):
    model_config = SettingsConfigDict(
        env_prefix="PROXY_NET_")


class _Services(BaseSettings):
    proxy_io: _ProxyIo = _ProxyIo()
    spaceproxy: _SpaceProxy = _SpaceProxy()
    proxy_net: _ProxyNet = _ProxyNet()


class _Logs(BaseSettings):
    rotation: str = _config_ini.get('logs', 'rotation')
    level: str = _config_ini.get('logs', 'level')
    path: str = datetime.now().strftime('logs/%Y_%m_%d_log.log')


class _Redis(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    password: str


class _Settings(BaseSettings):
    MODE: Literal['DEV', "TEST", "PROD"] = 'DEV'
    db: _Database = _Database()
    logs: _Logs = _Logs()
    name: str = _config_ini.get('default', 'name')
    APIKEY: str
    redis: _Redis = _Redis()
    services: _Services = _Services()


settings = _Settings()
