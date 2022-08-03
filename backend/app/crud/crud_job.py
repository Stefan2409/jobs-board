from typing import Any, Dict, List, Optional, Union
from pydantic.networks import EmailStr
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas.job import IJobCreate, IJobUpdate
from app.models import Job
from app.core.security import verify_password, get_password_hash
from datetime import datetime
from uuid import UUID


class CRUDJob(CRUDBase[Job, IJobCreate, IJobUpdate]):
    async def get_job_by_id(self, db_session: AsyncSession, id: UUID) -> Optional[Job]:
        return await super().get(db_session, id=id)

    async def create(self, db_session: AsyncSession, *, obj_in: IJobCreate) -> Job:
        db_obj = Job(
            title=obj_in.title,
            description=obj_in.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_session: AsyncSession,
        *,
        db_obj: Job,
        obj_in: Union[IJobUpdate, Dict[str, Any]]
    ) -> Job:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["updated_at"] = datetime.utcnow()
        update_data["title"] = obj_in.title
        update_data["description"] = obj_in.description

        response = super().update(db_session, db_obj=db_obj, obj_in=update_data)
        return response


job = CRUDJob(Job)
