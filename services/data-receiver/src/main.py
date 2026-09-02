from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connection to redis

    # redis retry logic

    yield

    # close connection to redis

app = FastAPI(lifespan=lifespan)

app.include_router(router)