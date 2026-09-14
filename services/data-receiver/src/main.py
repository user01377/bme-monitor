from fastapi import FastAPI
from contextlib import asynccontextmanager
from .redis_client import connect_redis
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await connect_redis()

    app.state.redis = redis

    yield

    await redis.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(router)