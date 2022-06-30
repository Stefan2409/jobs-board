from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from .jobs_occupation_group import JobsOccupationGroup

if TYPE_CHECKING:
    from .occupation_group import OccupationGroup


class JobsBase(SQLModel):
    title: str = Field(index=True)
    description: str = Field(index=True)


class Job(JobsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = datetime.now()

    occupation_groups: List["OccupationGroup"] = Relationship(
        back_populates="jobs", link_model=JobsOccupationGroup)


class JobsRead(JobsBase):
    id: int
    created_at: datetime
    occupation_groups: List["OccupationGroup"]


class JobsCreate(JobsBase):
    occupation_groups: List["OccupationGroup"]


class JobsUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    occupation_groups: List["OccupationGroup"]
