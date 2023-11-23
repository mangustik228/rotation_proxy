from .base_repo import BaseRepo
import app.models as M


class Location(BaseRepo):
    model = M.Location
