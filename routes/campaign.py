from db.session import SessionDep
from fastapi import HTTPException, Query, APIRouter
from models.campaign import CampaignRequest, ApiResponse
from sqlmodel import desc, select
from schema.campaign import Campaign

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/", response_model=ApiResponse[list[Campaign]])
async def read_campaign(
    session: SessionDep,
    limit: int | None = Query(3, le=100), #set limit = 0 to fecth all
    offset: int | None = Query(0, ge=0),
    name: str | None = None,
    sort: str = Query("id", pattern="^(id|created_at)$")
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

    data = session.exec(query).all()

    return ApiResponse(
        data=data,
        limit=limit,
        offset=offset
    )

@router.get("/{id}", response_model=ApiResponse[Campaign])
async def get_campaign(id: int, session: SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return ApiResponse(
        data=data,
        limit=1,
        offset=0
    )

@router.post("/", response_model=ApiResponse[Campaign], status_code=201)
async def create_campaign(campaign: CampaignRequest, session: SessionDep):
    db_campaign = Campaign(**campaign.model_dump())
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return ApiResponse(
        data=db_campaign,
        limit=1,
        offset=0
    )

@router.put("/{id}", response_model=ApiResponse[Campaign])
async def update_campaign(id: int, campaign: CampaignRequest, session: SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    data.name = campaign.name
    data.due_date = campaign.due_date
    session.add(data)
    session.commit()
    session.refresh(data)
    return ApiResponse(
        data=data,
        limit=1,
        offset=0
    )

@router.delete("/{id}", status_code=204)
async def delete_campaign(id: int, session: SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(data)
    session.commit()

   