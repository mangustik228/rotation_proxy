from fastapi import Depends, FastAPI

import app.dependencies as dependencies
from app.config import ConfigLogging, settings
from app.exceptions import register_exceptions_handlers
from app.middlewares import register_middlewares
from app.routers import register_routers

app = FastAPI(dependencies=[Depends(dependencies.get_api_key)])

register_middlewares(app)
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
