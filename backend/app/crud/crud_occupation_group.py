from typing import List
from app.models.occupation_group import OccupationGroup
from app.models.job import Job
from app.schemas.occupation_group import IOccupationGroupCreate, IOccupationGroupUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID


class CRUDOccupationGroup(
    CRUDBase[OccupationGroup, IOccupationGroupCreate, IOccupationGroupUpdate]
):
    async def get_occupation_group_by_name(
        self, db_session: AsyncSession, *, name: str
    ) -> OccupationGroup:
        occupation_group = await db_session.exec(
            select(OccupationGroup).where(OccupationGroup.name == name)
        )
        return occupation_group.first()

    async def add_job_to_occupation_group(
        self, db_session: AsyncSession, *, job: Job, occupation_group_id: UUID
    ) -> OccupationGroup:
        occupation_group = await super().get(db_session, id=occupation_group_id)
        occupation_group.jobs.append(job)
        db_session.add(occupation_group)
        await db_session.commit()
        await db_session.refresh(occupation_group)
        return occupation_group

    async def add_jobs_to_occupation_group(
        self, db_session: AsyncSession, *, jobs: List[Job], occupation_group_id: UUID
    ) -> OccupationGroup:
        occupation_group = await super().get(db_session, id=occupation_group_id)
        occupation_group.jobs.extend(jobs)
        db_session.add(occupation_group)
        await db_session.commit()
        await db_session.refresh(occupation_group)
        return occupation_group


occupation_group = CRUDOccupationGroup(OccupationGroup)
