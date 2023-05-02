from logging.config import dictConfig

from fastapi import FastAPI

from .logging import LogConfig
from .routes import router


def build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    dictConfig(LogConfig().dict())

    return app
