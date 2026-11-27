from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.base import NotFoundError, PermissionDeniedError
from src.exceptions.request import BusinessValidationError

ERROR_STATUS_MAP = {
    NotFoundError: 404,
    PermissionDeniedError: 403,
    BusinessValidationError: 422,
}

async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    for error_type, status_code in ERROR_STATUS_MAP.items():
        if isinstance(exc, error_type):
            return JSONResponse(
                status_code=status_code, content={"detail": str(exc)}
            )
    return JSONResponse(status_code=500, content={"detail": str(exc)})