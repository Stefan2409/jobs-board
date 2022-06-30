from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .jobs_occupation_group import JobsOccupationGroup

if TYPE_CHECKING:
    from .jobs import Job


class OccupationGroupBase(SQLModel):
    name: str = Field(index=True)


class OccupationGroup(OccupationGroupBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    jobs: List["Job"] = Relationship(
        back_populates="occupationgroups", link_model=JobsOccupationGroup)


class OccupationGroupRead(OccupationGroupBase):
    id: int


class OccupationGroupCreate(OccupationGroupBase):
    pass
