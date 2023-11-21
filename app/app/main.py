from fastapi import FastAPI
import routers
from app.config import settings

app = FastAPI()

app.include_router(routers.proxies)


@app.get("/home")
async def home():
    print(settings)
    return {"status": "ok",
            "settings": settings}
