from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from schema.campaign import Campaign


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
