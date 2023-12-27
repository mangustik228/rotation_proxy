from datetime import datetime, timedelta
from .base_builder import BaseBuilder


class ProxyBuilder(BaseBuilder):
    def set_default_value(self):
        self.data["expire"] = datetime.now() + timedelta(days=5)
        self.data["server"] = "127.0.0.1"
        self.data["username"] = "username-123"
        self.data["password"] = "password-123"
        self.data["port"] = 8000
        self.data["service_id"] = 1
        self.data["location_id"] = 1
        self.data["type_id"] = 1

    def set_type_id(self, id: int):
        self.data["type_id"] = 2

    def set_expire(self, date: datetime):
        if isinstance(date, datetime):
            self.data["expire"] = date
        else:
            raise TypeError("date must be datetime")

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

    def build_to_endpoint(self):
        if isinstance(self.data["expire"], datetime):
            self.data["expire"] = self.data["expire"].isoformat()
        return self.data.copy()
