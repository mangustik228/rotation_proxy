from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi

import app.dependencies as dependencies
from app.config import ConfigLogging
from app.docs.main import DESCRIPTION_MAIN
from app.docs.tags import tags_metadata
from app.exceptions import register_exceptions_handlers
from app.middlewares import register_middlewares
from app.routers import register_routers

app = FastAPI(
    dependencies=[Depends(dependencies.get_api_key)],
    title="Rotation proxy",
    version="0.2.0",
    description=DESCRIPTION_MAIN,
    openapi_tags=tags_metadata)


register_middlewares(app)
register_routers(app)
register_exceptions_handlers(app)


@app.on_event("startup")
async def startup_event():
    ConfigLogging.setup()
