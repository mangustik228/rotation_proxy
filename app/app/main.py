from fastapi import FastAPI
import routers
from app.config import settings
from app.services.startup.startup import prepare_db
from loguru import logger

app = FastAPI()

app.include_router(routers.proxies)
app.include_router(routers.proxy_service)
app.include_router(routers.location)


@app.get("/home")
async def home():
    print(settings)
    return {"status": "ok",
            "settings": settings}


@app.on_event("startup")
async def startup_event():
    await prepare_db()
    ...
