from fastapi import Depends, FastAPI

import app.dependencies as dependencies
from app.config import ConfigLogging
from app.exceptions import register_exceptions_handlers
from app.middlewares import register_middlewares
from app.routers import register_routers

app = FastAPI(dependencies=[Depends(dependencies.get_api_key)])

register_middlewares(app)
register_routers(app)
register_exceptions_handlers(app)


@app.on_event("startup")
async def startup_event():
    ConfigLogging.setup()
