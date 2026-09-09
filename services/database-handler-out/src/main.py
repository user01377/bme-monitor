from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import router

@asynccontextmanager
def lifespan(app: FastAPI):

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)