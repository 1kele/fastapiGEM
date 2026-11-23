from fastapi import Request, status
from fastapi.responses import JSONResponse

from exceptions.base import NotFoundError
from exceptions.offer import InvalidStatusTransitionError


async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


async def invalid_status_handler(request: Request, exc: InvalidStatusTransitionError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )
