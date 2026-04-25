from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime

if TYPE_CHECKING:
    from .campaign import Campaign


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore

    id: UUID | None = Field(primary_key=True, default_factory=uuid4)
    name: str
    created_at: datetime = Field(default_factory=lambda:datetime.now())
    due_date: datetime | None
    campaign_id: UUID = Field(foreign_key="campaigns.id")
    campaign: Optional["Campaign"] = Relationship(back_populates="tasks")
