from logging import getLogger
from typing import Any, Callable, Coroutine

from fastapi import Request, Response
from fastapi.routing import APIRoute

logger = getLogger("service")


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable[..., Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(request)

            if headers := request.headers:
                logger.debug("Request headers: %s", dict(headers))

            if data := await request.body():
                logger.debug("Request data: %s", data.decode())

            if headers := response.headers:
                logger.debug("Response data: %s", dict(headers))

            if data := response.body:
                logger.debug("Response data: %s", data.decode())

            return response

        return custom_route_handler
