from sqlalchemy import text
from sqlmodel import SQLModel, Field, Relationship
from typing import List
from uuid import UUID
from datetime import datetime
from .task import Task


class Campaign(SQLModel, table=True):
    __tablename__ = "campaigns" #  # type: ignore
    
    id: UUID = Field(default=None,primary_key=True,  sa_column_kwargs={
       "server_default" : text("gen_random_uuid()")
    })
    name: str
    due_date: datetime | None = None
    created_at: datetime = Field(sa_column_kwargs={
        "server_default": text("CURRENT_TIMESTAMP")
    })
    tasks: List["Task"] = Relationship(back_populates="campaign")
