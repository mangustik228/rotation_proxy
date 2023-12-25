from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

from app.config import settings, ConfigLogging
import app.routers as routers
import app.dependencies as dependencies

app = FastAPI(dependencies=[Depends(dependencies.get_api_key)])

app.include_router(routers.proxies_rotations)
app.include_router(routers.proxies)
app.include_router(routers.proxy_service)
app.include_router(routers.location)
app.include_router(routers.proxy_type)
app.include_router(routers.error)
app.include_router(routers.parsed_services)

api_key_header = APIKeyHeader(name="X-API-Key")


@app.get("/home")
async def home():
    print(settings)
    return {"status": "ok",
            "settings": settings}


@app.on_event("startup")
async def startup_event():
    ConfigLogging.setup()
