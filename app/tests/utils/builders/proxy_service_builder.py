from .base_builder import BaseBuilder


class ProxyServiceBuilder(BaseBuilder):
    '''
    Дефолтно возвращает proxy6.net
    '''

    def set_default_value(self):
        self.data["name"] = "proxy6.net"

    def set_name(self, name: str):
        self.data["name"] = name
