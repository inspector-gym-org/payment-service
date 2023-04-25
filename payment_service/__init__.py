from contextlib import asynccontextmanager
from logging.config import dictConfig
from typing import AsyncGenerator

from fastapi import FastAPI

from .config import settings
from .database import create_indexes
from .logging import LogConfig
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_indexes()
    yield


def build_app() -> FastAPI:
    app = FastAPI(root_path=settings.app_root_path, lifespan=lifespan)
    app.include_router(router)

    dictConfig(LogConfig().dict())

    return app
