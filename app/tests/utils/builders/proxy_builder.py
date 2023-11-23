from datetime import datetime, timedelta
from .base_builder import BaseBuilder


class ProxyBuilder(BaseBuilder):
    def set_default_value(self):
        self.data["expire"] = (datetime.now() + timedelta(days=5)).isoformat()
        self.data["server"] = "127.0.0.1"
        self.data["username"] = "username-123"
        self.data["password"] = "password-123"
        self.data["port"] = 8000
        self.data["service_id"] = 1
        self.data["location_id"] = 1
        self.data["type_id"] = 1

    def set_expire(self, date: str | datetime):
        if isinstance(date, datetime):
            self.data["expire"] = date.isoformat()
        else:
            self.data["expire"] = date

    def set_service_id(self, service_id: int) -> None:
        self.data["service"] = service_id

    def set_server(self, server: str) -> None:
        self.data["server"] = server

    def set_username(self, username: str) -> None:
        self.data["username"] = username

    def set_password(self, password: str) -> None:
        self.data["password"] = password

    def set_port(self, port: str) -> None:
        self.data["port"] = port
