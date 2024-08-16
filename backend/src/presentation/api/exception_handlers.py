from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.client import BadRequestException, ConflictException, NotFoundException
from src.infrastructure.log import logger


async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=400,
        content={"status": 400, "message": exc.message},
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"status": 404, "message": exc.message},
    )


async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=409,
        content={"status": 409, "message": exc.message},
    )


async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"{exc.__class__.__name__}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": 500, "message": "Internal Server Error"},
    )
