from typing import Optional
from app.schemas.common import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.job import IJobCreate, IJobRead, IJobReadWithoutOccupationGroups
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import User
from app.models.job import Job
from sqlmodel import select, and_
from uuid import UUID
from app.schemas.role import IRoleEnum
from app.models.role import Role

router = APIRouter()


@router.get(
    "/job/list", response_model=IGetResponseBase[Page[IJobReadWithoutOccupationGroups]]
)
async def read_jobs_list(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
):
    """
    Retrieve jobs.
    """
    jobs = await crud.job.get_multi_paginated(db_session, params=params)
    return IGetResponseBase[Page[IJobReadWithoutOccupationGroups]](data=jobs)


@router.get(
    "/job/order_by_created_at",
    response_model=IGetResponseBase[Page[IJobReadWithoutOccupationGroups]],
)
async def get_job_list_order_by_created_at(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
):
    query = select(Job).order_by(Job.created_at)
    jobs = await crud.job.get_multi_paginated(db_session, query=query, params=params)
    return IGetResponseBase[Page[IJobReadWithoutOccupationGroups]](data=jobs)


@router.get("/job/{job_id}", response_model=IGetResponseBase[IJobRead])
async def get_job_by_id(
    job_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
):
    job = await crud.job.get_job_by_id(db_session, id=job_id)
    return IGetResponseBase[IJobRead](data=job)


@router.post("/job", response_model=IPostResponseBase[IJobRead])
async def create_job(
    new_job: IJobCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    job = await crud.job.create(db_session, obj_in=new_job)
    return IPostResponseBase[IJobRead](data=job)


@router.delete("/job/{job_id}", response_model=IDeleteResponseBase[IJobRead])
async def remove_job(
    job_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):

    job = await crud.job.get_job_by_id(db_session=db_session, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job = await crud.job.remove(db_session, id=job_id)
    return IDeleteResponseBase[IJobRead](data=job)
