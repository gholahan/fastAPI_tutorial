from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class Campaign (SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True)
   name: str = Field(index=True)
   due_date: datetime | None  = Field(default=None, index=True)
   created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),index=True)
