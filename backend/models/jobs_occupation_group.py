from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class JobsOccupationGroup(SQLModel, table=True):
    jobs_id: Optional[int] = Field(
        default=None, foreign_key="job.id", primary_key=True)
    occupation_group_id: Optional[int] = Field(
        default=None, foreign_key="occupationgroup.id", primary_key=True)
