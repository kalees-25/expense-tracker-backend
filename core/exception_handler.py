from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError


# ---------------- VALIDATION ERROR HANDLER ----------------

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": exc.errors()
        }
    )

# ---------------- DATABASE ERROR HANDLER ----------------

async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Database error occurred"
        }
    )


# ---------------- GENERIC ERROR HANDLER ----------------

async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Something went wrong"
        }
    )