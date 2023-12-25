from .base_repo import BaseRepo
import app.models as M


class ParsedService(BaseRepo):
    model = M.ParsedService
