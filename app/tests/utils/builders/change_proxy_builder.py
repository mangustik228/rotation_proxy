from typing import Any
from .base_builder import BaseBuilder


class ChangeProxyBuilder(BaseBuilder):
    def set_default_value(self):
        self.data["proxy_id"] = 1
        self.data["parsed_service_id"] = 1
        self.data["reason"] = "cloudlfare"
        self.data["logic"] = "linear"

    def set_proxy_id(self, other: Any):
        self.data["proxy_id"] = other

    def set_parsed_service_id(self, other: Any):
        self.data["parsed_service_id"] = other

    def set_ignore_hours(self, other: Any):
        self.data["ignore_hours"] = other

    def set_parsed_service(self, other: Any):
        self.data["parsed_service"] = other

    def set_expire_proxy(self, other: Any):
        self.data["expire_proxy"] = other

    def set_location_id(self, other: Any):
        self.data["location_id"] = other

    def set_type_id(self, other: Any):
        self.data["type_id"] = other

    def set_lock_time(self, other: Any):
        self.data["lock_time"] = other

    def set_reason(self, other: Any):
        self.data["reason"] = other

    def set_logic(self, other: Any):
        self.data["logic"] = other

    def set_params(self, other: Any):
        self.data["params"] = other
