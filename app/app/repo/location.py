import app.models as M

from .base_repo import BaseRepo


class Location(BaseRepo):
    model = M.Location
