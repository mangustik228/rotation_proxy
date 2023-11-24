from .base_builder import BaseBuilder


class ProxyTypesBuilder(BaseBuilder):
    def set_default_value(self):
        self.data["name"] = "IPv6"

    def set_name(self, name: str):
        self.data["name"] = name
