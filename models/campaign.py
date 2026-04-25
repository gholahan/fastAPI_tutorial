from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")
class PaginatedResponse(BaseModel, Generic[T]):
   data:T
   message:str = "success"
   limit: int | None
   offset: int

class ApiResponse(BaseModel, Generic[T]):
    data: T
    message: str = "success"
   #  task: list

  
class CampaignRequest(BaseModel):
   name : str
   due_date: datetime | None = None

class CampaignUpdate(BaseModel):
   name : str | None =  None
   due_date: datetime | None = None

