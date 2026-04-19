from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")
class ApiResponse(BaseModel, Generic[T]):
   data:T
   message:str = "success"
   limit: int | None
   offset: int | None


class CampaignRequest(BaseModel):
   name : str
   due_date: datetime | None

