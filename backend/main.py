from datetime import datetime
from turtle import title
from fastapi import FastAPI
from pydantic import BaseModel

from backend.models.jobs_occupation_group import JobsOccupationGroup
from backend.models.occupation_group import OccupationGroup
from backend.models.jobs import Job
from typing import List


from .routers import jobs as jobs_router
from sqlmodel import SQLModel, Session
from .database import engine, get_session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_database_data():
    occupation1 = OccupationGroup(name="Marketing")
    occupation2 = OccupationGroup(name="Finance")
    occupation3 = OccupationGroup(name="IT")
    occupation4 = OccupationGroup(name="Organisation")

    job1 = Job(title="Controller", description="Bla bla bla",
               created_at=datetime.now(), occupationgroup=[occupation1, occupation3])
    job2 = Job(title="Hackler", description="Bla bla bla",
               created_at=datetime.now(), occupationgroup=[occupation2])

    with Session(engine) as session:
        session.add(job1)
        session.add(job2)
        session.commit()
        session.close()


app = FastAPI()


@app.on_event("startup")
def main():
    create_db_and_tables()
    create_database_data()


app.include_router(jobs_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
