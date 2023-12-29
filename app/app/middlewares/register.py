from fastapi import FastAPI
from .log_middleware import LogMiddleware


def register_middlewares(app: FastAPI):
    app.add_middleware(LogMiddleware)
