from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from .link_job_occupation_group import LinkJobOccupationGroup
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID


class OccupationGroupBase(SQLModel):
    name: str


class OccupationGroup(BaseUUIDModel, OccupationGroupBase, table=True):
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "OccupationGroup.created_by_id==User.id",
        }
    )
    jobs: List["Job"] = Relationship(
        back_populates="occupation_groups",
        link_model=LinkJobOccupationGroup,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
