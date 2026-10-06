import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(base_url="http://database-handler-out:8002")

    yield

    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")