from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: Exception):
    
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        message = exc.detail
    else:
        status_code = 500
        message = "Internal Server Error"

    return JSONResponse(
        status_code=status_code,
        content={
            "data": None,
            "message": message,
            "status": "error"
        },
    )
