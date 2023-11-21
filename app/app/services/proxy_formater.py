import app.models as M


class ProxyFormater:
    available_formats = {"full", "queue", "short"}
    available_types = {"requests", "playwright"}

    @classmethod
    def prepare_proxies(cls, data: list[M.Proxy], format: str, app_type: str):
        cls.check_type(app_type)
        cls.check_format(format)
        if format == "full":
            return data
        result = []
        for datum in data:
            proxy = cls.extract_proxy(datum, app_type)
            if format == "short":
                result.append(proxy)
            if format == "queue":
                result.append({"id": datum.id,
                               "proxy": proxy,
                               "expire": datum.expire,
                               "service": datum.service})
        return result

    @classmethod
    def check_type(cls, type_: str):
        if type_ not in cls.available_types:
            raise ValueError(
                f'type_ `{type_}` NOT SUPPORTED. MUST BE {cls.available_types}')

    @classmethod
    def check_format(cls, format: str):
        if format not in cls.available_formats:
            raise ValueError(
                f'format `{format}` NOT SUPPORTED. MUST BE {cls.available_formats}')

    @classmethod
    def extract_proxy(cls, datum: M.Proxy, type_: str):
        if type_ == "requests":
            return {
                "http": cls._get_requests_string("http", datum),
                "https": cls._get_requests_string("https", datum)}
        if type_ == "playwright":
            return {
                "server": f"http://{datum.server}:{datum.port}",
                "username": datum.username,
                "password": datum.password}

    @staticmethod
    def _get_requests_string(prefix, datum: M.Proxy):
        return f"{prefix}://{datum.username}:{datum.password}@{datum.server:{datum.port}}"
