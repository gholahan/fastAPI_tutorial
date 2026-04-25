from fastapi import FastAPI, HTTPException
from core.exceptions import http_exception_handler
from db.session import SessionDep
from routes.campaign import router as campaigns_router
from routes.task import router as tasks_router



app = FastAPI(root_path="/api/v1")
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(campaigns_router)
app.include_router(tasks_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

from sqlmodel import select

@app.get("/db-test")
async def db_test(session: SessionDep):
    result = await session.exec(select(1))
    return result.first()
