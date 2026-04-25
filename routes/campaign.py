from uuid import UUID
from db.session import SessionDep
from fastapi import HTTPException, Query, APIRouter
from models.campaign import CampaignRequest, CampaignUpdate, PaginatedResponse, ApiResponse
from sqlmodel import desc, select
from schema.campaign import Campaign
from schema.task import Task
# from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("/", response_model=PaginatedResponse[list[Campaign]])
async def read_campaign(
    session: SessionDep,
    limit: int = Query(3, le=100),  # set limit = 0 to fetch all
    offset: int = Query(0, ge=0),
    name: str | None = None,
    sort: str = Query("created_at", pattern="^(id|created_at|due_date)$")
):
    query = select(Campaign)

    if name:
        query = query.where(Campaign.name == name)

    if sort == "id":
        query = query.order_by(desc(Campaign.id))
    elif sort == "created_at":
        query = query.order_by(desc(Campaign.created_at))

    query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    data = (await session.exec(query)).all()

    return PaginatedResponse(
        data=data,
        limit=limit,
        offset=offset
    )

@router.get("/{id}",response_model=ApiResponse[Campaign])
async def get_campaign (id: UUID, session:SessionDep):
    # query = select(Campaign).where(Campaign.id == id)

    data = await session.get(Campaign, id)

    if not data:
        raise HTTPException(status_code=404, detail="campaign not found")
    
    return ApiResponse(
        data = data
    )



@router.get("/{campaign_id}/tasks", response_model = ApiResponse[list[Task]])
async def get_tasks_for_campaign(
    campaign_id: UUID,
    session: SessionDep
):
    campaign = await session.get(Campaign, campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    statement = (
         select(Task)
        .join(Campaign)
        .where(Campaign.id == campaign_id)
    )

    tasks = (await session.exec(statement)).all()

    return ApiResponse(data=tasks)



@router.post("/", response_model=ApiResponse[Campaign], status_code=201)
async def create_campaign(
    campaign: CampaignRequest,
    session: SessionDep
):
    db_campaign = Campaign(**campaign.model_dump())

    session.add(db_campaign)

    await session.commit()
    await session.refresh(db_campaign)

    return ApiResponse(data=db_campaign)


@router.put("/{id}", response_model=ApiResponse[Campaign])
async def update_campaign(id: UUID,campaign: CampaignRequest,session: SessionDep):
    data = await session.get(Campaign, id)

    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    data.name = campaign.name 
    data.due_date = campaign.due_date

    session.add(data)

    await session.commit()
    await session.refresh(data)

    return ApiResponse(data=data)


@router.patch("/{id}", response_model=ApiResponse[Campaign])
async def patch_campaign(id: UUID, session:SessionDep, campaign:CampaignUpdate):
    data = await session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    for key, value in campaign.model_dump(exclude_unset=True).items():
            setattr(data, key, value)

    await session.commit()
    await session.refresh(data)

    return ApiResponse(
        data= data
    )


@router.delete("/{id}", status_code=204)
async def delete_campaign(
    id: UUID,
    session: SessionDep
):
    data = await session.get(Campaign, id)

    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    await session.delete(data)
    await session.commit()
