from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

from app.config import settings, ConfigLogging
import app.dependencies as dependencies
from .exceptions import register_exceptions_handlers
from app.routers import register_routers

app = FastAPI(dependencies=[Depends(dependencies.get_api_key)])

register_routers(app)
register_exceptions_handlers(app)


@app.get("/home")
async def home():
    print(settings)
    return {"status": "ok",
            "settings": settings}


@app.on_event("startup")
async def startup_event():
    ConfigLogging.setup()
