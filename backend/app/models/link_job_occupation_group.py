from sqlmodel import Field
from typing import Optional
from app.models.base_uuid_model import BaseJoinUUIDModel
from uuid import UUID


class LinkJobOccupationGroup(BaseJoinUUIDModel, table=True):
    occupation_group_id: Optional[UUID] = Field(
        default=None,
        nullable=False,
        foreign_key="occupationgroup.id",
        primary_key=True,
    )
    job_id: Optional[UUID] = Field(
        default=None, nullable=False, foreign_key="job.id", primary_key=True
    )
