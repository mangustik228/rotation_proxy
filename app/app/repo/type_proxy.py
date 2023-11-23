from .base_repo import BaseRepo
import app.models as M


class Type(BaseRepo):
    model = M.ProxyType
