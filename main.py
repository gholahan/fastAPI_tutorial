from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from db.session import lifespan
from routes.campaign import router as campaigns_router


app = FastAPI(root_path="/api/v1", lifespan=lifespan)
app.include_router(campaigns_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "message": exc.detail,
            "status": "error"
        },
)

@app.get("/health")
async def health():
    return {"status": "ok"}