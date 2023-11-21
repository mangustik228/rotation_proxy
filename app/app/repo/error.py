from .repo_base import BaseRepo
import app.models as M


class Error(BaseRepo):
    model = M.Error
