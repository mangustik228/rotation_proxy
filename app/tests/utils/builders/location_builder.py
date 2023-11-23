from .base_builder import BaseBuilder


class LocationBuilder(BaseBuilder):
    def set_default_value(self):
        self.data["name"] = "Cambodia"

    def set_name(self, name: str):
        self.data["name"] = name
