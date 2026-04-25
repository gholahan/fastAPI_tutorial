from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    data: T
    message: str = "success"
   
   
class TaskRequest(BaseModel):
   name : str
   due_date: datetime | None
   campaign_id : UUID
