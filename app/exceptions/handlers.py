from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.product import ProductNotFoundException
from app.exceptions.user import UserNotFoundException
from app.models.error import ErrorResponse
from app.exceptions.auth import InvalidCredentialsException


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    error = ErrorResponse(
        status_code=exc.status_code,
        detail=f"User with ID {exc.user_id} not found."
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error.model_dump()
    )


async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundException
):
    error = ErrorResponse(
        status_code=exc.status_code,
        detail=f"Product with ID {exc.product_id} not found."
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error.model_dump()
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    error = ErrorResponse(
        status_code=401,
        detail=exc.message
    )
    return JSONResponse(
        status_code=401,
        content=error.model_dump()
    )