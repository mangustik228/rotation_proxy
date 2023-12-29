from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .exceptions import (DuplicateKey, NotAvailableProxies,
                         NotExistedParsedService, NotValidExpire,
                         NotValidServiceName)


def register_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(
        NotAvailableProxies, not_available_proxies)
    app.add_exception_handler(
        NotValidServiceName, not_valid_service_name)
    app.add_exception_handler(
        NotValidExpire, not_valid_expire)
    app.add_exception_handler(
        NotExistedParsedService, not_exist_parsed_service)
    app.add_exception_handler(
        DuplicateKey, duplicate_key)


async def duplicate_key(req, exc: DuplicateKey):
    return JSONResponse({"detail": str(exc)}, 409)


async def not_available_proxies(req, exc: NotAvailableProxies):
    return JSONResponse({"detail": str(exc)}, 404)


async def not_valid_service_name(req, exc: NotValidServiceName):
    return JSONResponse({"detail": str(exc)}, 409)


async def not_valid_expire(req, exc: NotValidExpire):
    return JSONResponse({"detail": str(exc)}, 409)


async def not_exist_parsed_service(req, exc: NotExistedParsedService):
    return JSONResponse({"detail": str(exc)}, 409)
