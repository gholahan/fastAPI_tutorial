from fastapi import APIRouter, HTTPException
from models.task import ApiResponse, TaskRequest
from schema.task import Task
from schema.campaign import Campaign
from db.session import SessionDep
from sqlmodel import select
router = APIRouter(prefix="/tasks", tags=['Tasks'])

@router.get("/")
async def get_task(session: SessionDep):
    data = (await session.exec(select(Task))).all()
    return{"task": data}



@router.post("/", response_model=ApiResponse[Task])
async def create_task(request: TaskRequest, session: SessionDep):
    
    campaign = await session.get(Campaign, request.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db_task = Task(**request.model_dump())

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return {
        "data": db_task
    }
