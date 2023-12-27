from abc import ABC, abstractmethod


class BaseBuilder(ABC):
    data: dict = None

    def __init__(self):
        self.data = {}
        self.set_default_value()

    @abstractmethod
    def set_default_value(self):
        ...

    def delete_field(self, name: str) -> None:
        self.data.pop(name)

    def build(self):
        return self.data.copy()

    def build_list(self):
        return [self.data]

    def build_to_repo(self):
        return self.build()
