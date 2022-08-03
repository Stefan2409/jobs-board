from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from app.models.link_job_occupation_group import LinkJobOccupationGroup
from typing import List, Optional
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID


class JobBase(SQLModel):
    title: str = Field(nullable=False, index=True)
    description: str


class Job(BaseUUIDModel, JobBase, table=True):
    occupation_groups: List["OccupationGroup"] = Relationship(
        back_populates="jobs",
        link_model=LinkJobOccupationGroup,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
