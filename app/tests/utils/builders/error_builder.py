from .base_builder import BaseBuilder


class ErrorBuilder(BaseBuilder):
    def set_default_value(self):
        self.data["proxy_id"] = 1
        self.data["reason"] = "ERROR"
        self.data["parsed_service_id"] = 1
        self.data["sleep_time"] = 200

    def set_proxy_id(self, other):
        self.data["proxy_id"] = other

    def set_reason(self, other):
        self.data["reason"] = other
