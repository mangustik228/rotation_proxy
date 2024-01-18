import asyncio
from functools import wraps

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from .exceptions import (DbProblem, DuplicateKey, NoIdentifyCountryCode,
                         NoIdentifyTypeId, NotAvailableProxies,
                         NotExistedParsedService, NotValidExpire,
                         NotValidServiceName, ProblemWithService)


def register_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(NotAvailableProxies, error_404)
    app.add_exception_handler(NotValidServiceName, error_409)
    app.add_exception_handler(NotValidExpire, error_409)
    app.add_exception_handler(DuplicateKey, error_409)
    app.add_exception_handler(NotExistedParsedService, error_409)
    app.add_exception_handler(DbProblem, error_500)
    app.add_exception_handler(ProblemWithService, error_500)
    app.add_exception_handler(NoIdentifyCountryCode, error_500)
    app.add_exception_handler(NoIdentifyTypeId, error_500)


async def error_500(req, exc: DbProblem):
    return JSONResponse({"detail": str(exc)}, 500)


async def error_409(req, exc: DuplicateKey):
    return JSONResponse({"detail": str(exc)}, 409)


async def error_404(req, exc: NotAvailableProxies):
    return JSONResponse({"detail": str(exc)}, 404)
