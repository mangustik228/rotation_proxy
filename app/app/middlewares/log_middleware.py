from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from loguru import logger
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

# from starlette.responses import StreamingResponse


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def request_process(self, request: Request, data: dict, method: str):
        data["type"] = "request"
        if method == "GET":
            data["request_data"] = request.query_params.multi_items()
        if method in ("POST", "PUT"):
            await self.set_body(request)
            data["request_data"] = await request.json()
        logger.info(data)
        return data

    async def response_process(self, response: StreamingResponse, data: dict):
        data["type"] = "response"
        data["status"] = (status := response.status_code)
        if status < 300:
            logger.info(data)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        data = {}
        data["client_ip"] = request.client.host
        data["method"] = (method := request.method)
        data["url"] = request.url

        await self.request_process(request, data, method)
        response = await call_next(request)

        await self.response_process(response, data)
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
