from datetime import datetime, timedelta


class ProxyBuilder:
    def __init__(self):
        self.data = {}
        self.data["expire"] = (datetime.now() + timedelta(days=5)).isoformat()
        self.data["server"] = "127.0.0.1"
        self.data["username"] = "username-123"
        self.data["password"] = "password-123"
        self.data["port"] = 8000
        self.data["service"] = "google.com"
        self.data["location"] = "Russia"
        self.data["type_id"] = 1

    def delete_field(self, name: str) -> None:
        self.data.pop(name)

    def set_expire(self, date: str | datetime):
        if isinstance(date, datetime):
            self.data["expire"] = date.isoformat()
        else:
            self.data["expire"] = date

    def set_service(self, service: str) -> None:
        self.data["service"] = service

    def set_server(self, server: str) -> None:
        self.data["server"] = server

    def set_username(self, username: str) -> None:
        self.data["username"] = username

    def set_password(self, password: str) -> None:
        self.data["password"] = password

    def set_port(self, port: str) -> None:
        self.data["port"] = port

    def build(self):
        return [self.data]
