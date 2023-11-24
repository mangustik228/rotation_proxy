from .base_repo import BaseRepo
import app.models as M


class ProxyType(BaseRepo):
    model = M.ProxyType
