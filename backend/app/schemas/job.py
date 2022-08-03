from app.models.job import JobBase
from app.models.occupation_group import OccupationGroupBase
from pydantic import BaseModel
from .role import IRoleRead
from typing import Optional, List
from uuid import UUID
from enum import Enum


class IJobCreate(BaseModel):
    title: str
    description: str


class IJobReadWithoutOccupationGroups(JobBase):
    id: UUID


class IOccupationGroupRead(OccupationGroupBase):
    id: UUID


class IJobRead(JobBase):
    id: UUID
    occupation_groups: List[IOccupationGroupRead] = []


class IJobUpdate(BaseModel):
    id: UUID
