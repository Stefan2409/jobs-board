from typing import List
from app.models.occupation_group import OccupationGroupBase
from .job import IJobReadWithoutOccupationGroups
from uuid import UUID


class IOccupationGroupCreate(OccupationGroupBase):
    pass


class IOccupationGroupRead(OccupationGroupBase):
    id: UUID


class IOccupationGroupReadWithJobs(OccupationGroupBase):
    id: UUID
    jobs: List[IJobReadWithoutOccupationGroups]


class IOccupationGroupUpdate(OccupationGroupBase):
    pass
