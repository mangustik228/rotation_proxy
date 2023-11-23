from .base_repo import BaseRepo
import app.models as M


class ProxyService(BaseRepo):
    model = M.Service
