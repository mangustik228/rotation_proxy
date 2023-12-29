import app.models as M

from .base_repo import BaseRepo


class ProxyService(BaseRepo):
    model = M.Service
