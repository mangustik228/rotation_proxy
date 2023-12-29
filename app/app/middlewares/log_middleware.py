from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from loguru import logger
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

# from starlette.responses import StreamingResponse


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def request_process(self, request: Request, client_ip: str, method: str, url: str):
        if method == "GET":
            data = request.query_params.multi_items()
        if method in ("POST", "PUT", "PATCH", "DEL"):
            await self.set_body(request)
            data = await request.json()
        result = {
            "client_ip": client_ip,
            "method": method,
            "url": url,
            "data": data
        }
        logger.info(result)
        return data

    async def response_process(self, response: StreamingResponse, client_ip, method, url, request_data):
        data = {
            "client_ip": client_ip,
            "method": method,
            "url": url,
            "status_code": (status := response.status_code)
        }
        if status in (200, 201):
            logger.info(data)
        else:
            data["request_data"] = request_data
            logger.warning(data)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host
        method = request.method
        url = request.url

        request_data = await self.request_process(request, client_ip, method, url)
        response = await call_next(request)

        await self.response_process(response, client_ip, method, url, request_data)
        return response

    async def set_body(self, request: Request):
        '''
        https://stackoverflow.com/questions/69669808/fastapi-custom-middleware-getting-body-of-request-inside
        Способ достучаться до body в middleware.
        '''
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive
