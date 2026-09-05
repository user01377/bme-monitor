from fastapi import FastAPI
from contextlib import asynccontextmanager
from .redis_client import connect_redis
from .routes import router
from .database import Base, engine
from .models import Device

import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)

    redis = await connect_redis()

    app.state.redis = redis

    yield

    await redis.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(router)