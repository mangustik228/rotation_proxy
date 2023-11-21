from .repo_base import BaseRepo
import app.models as M


class Type(BaseRepo):
    model = M.ProxyType
