from .base_repo import BaseRepo
import app.models as M


class Error(BaseRepo):
    model = M.Error
