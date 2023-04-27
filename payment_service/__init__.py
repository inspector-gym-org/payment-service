from contextlib import asynccontextmanager
from logging.config import dictConfig
from typing import AsyncGenerator

from fastapi import FastAPI

from .database import create_indexes
from .logging import LogConfig
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_indexes()
    yield


def build_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    dictConfig(LogConfig().dict())

    return app
