from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, Generic, TypeVar
from fastapi import Depends, Query,Request, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, SQLModel ,Session ,create_engine, desc, select
from fastapi.responses import JSONResponse

class Campaign (SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True)
   name: str = Field(index=True)
   due_date: datetime | None  = Field(default=None, index=True)
   created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
     if not session.exec(select(Campaign)).first():
        session.add_all([
            Campaign(name="test", due_date=datetime.now()),
            Campaign(name="test 2", due_date=datetime.now())
        ])
        session.commit()
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

T = TypeVar("T")
class ApiResponse(BaseModel, Generic[T]):
   data:T
   message:str = "success"


class CampaignRequest(BaseModel):
   name : str
   due_date: datetime | None

class PaginatedRequest(BaseModel):
   limit: int
   offset: int

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

@app.get("/")
async def root():
    return {"message": "hello my first firstapi"}

@app.get("/campaigns", response_model=ApiResponse[list[Campaign]])
async def read_campaign(
    session: SessionDep,
    limit: int = Query(3, le=100),
    offset: int = Query(0, ge=0),
    name: str | None = None,
    sort: str =  Query("id", pattern="^(id|created_at)$")
):
   query = select(Campaign)

   if name:
      # if not session.get(Campaign, name):
      #  raise HTTPException(status_code=404, detail="campaign not found") 
    query = query.where(Campaign.name == name)

   if sort == "id":
      query = query.order_by(desc(Campaign.id))

   elif sort == "created_at":
      query = query.order_by(desc(Campaign.created_at))

   data = session.exec(
       query.offset(offset)
       .limit(limit)
       ).all()

   return {"data": data}




@app.get("/campaigns/{id}", response_model=ApiResponse[Campaign])
async def get_campaign(id:int, session:SessionDep):
   data = session.get(Campaign, id)
   if not data:
      raise HTTPException(status_code=404, detail="campaign not found") 
   return{"data": data}

@app.post("/camapigns", response_model=ApiResponse[Campaign], status_code=201)
async def create_campaign(campaign: CampaignRequest, session: SessionDep):
   db_capaign = Campaign(**campaign.model_dump())
   session.add(db_capaign)
   session.commit()
   session.refresh(db_capaign)
   return {"data": db_capaign}

@app.put("/campaign/{id}", response_model=ApiResponse[Campaign])
async def update_campaign(id: int, campaign:CampaignRequest, session: SessionDep):
   data = session.get(Campaign, id)
   if not data:
       raise HTTPException(status_code=404, detail="campaign not found")
   data.name = campaign.name
   data.due_date = campaign.due_date
   session.add(data)
   session.commit()
   session.refresh(data)
   return{"data": data}
   
@app.delete("/campaigns/{id}", status_code=204)
async def delete_campaign(id: int, session:SessionDep):
   data = session.get(Campaign, id)
   if not data:
      raise HTTPException(status_code=404)
   session.delete(data)
   session.commit()

   