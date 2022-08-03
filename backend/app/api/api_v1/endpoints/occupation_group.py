from app.models.user import User
from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.occupation_group import (
    IOccupationGroupCreate,
    IOccupationGroupRead,
    IOccupationGroupReadWithJobs,
    IOccupationGroupUpdate,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app import crud
from uuid import UUID
from app.schemas.role import IRoleEnum

router = APIRouter()


@router.get(
    "/occupation_group", response_model=IGetResponseBase[Page[IOccupationGroupRead]]
)
async def get_occupation_groups(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
):
    occupation_groups = await crud.occupation_group.get_multi_paginated(
        db_session, params=params
    )
    return IGetResponseBase[Page[IOccupationGroupRead]](data=occupation_groups)


@router.get(
    "/occupation_group/{occupation_group_id}",
    response_model=IGetResponseBase[IOccupationGroupReadWithJobs],
)
async def get_occupation_group_by_id(
    occupation_group_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    occupation_group = await crud.occupation_group.get(
        db_session, id=occupation_group_id
    )
    return IGetResponseBase[IOccupationGroupReadWithJobs](data=occupation_group)


@router.post(
    "/occupation_group", response_model=IPostResponseBase[IOccupationGroupRead]
)
async def create_occupation_group(
    occupation_group: IOccupationGroupCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    new_occupation_group = await crud.occupation_group.create(
        db_session, obj_in=occupation_group, created_by_id=current_user.id
    )
    return IPostResponseBase[IOccupationGroupRead](data=new_occupation_group)


@router.put(
    "/occupation_group/{occupation_group_id}",
    response_model=IPutResponseBase[IOccupationGroupRead],
)
async def update_occupation_group(
    occupation_group_id: UUID,
    occupation_group: IOccupationGroupUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    occupation_group_current = await crud.occupation_group.get(
        db_session=db_session, id=occupation_group_id
    )
    if not occupation_group_current:
        raise HTTPException(status_code=404, detail="Occupation Group not found")

    occupation_group_updated = await crud.occupation_group.update(
        db_session, obj_current=occupation_group_current, obj_new=occupation_group
    )
    return IPutResponseBase[IGroupRead](data=group_updated)


@router.post(
    "/group/add_job/{job_id}/{occupation_group_id}",
    response_model=IPostResponseBase[IOccupationGroupRead],
)
async def add_job_to_occupation_group(
    job_id: UUID,
    occupation_group_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    job = await crud.job.get(db_session=db_session, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    occupation_group = await crud.occupation_group.add_job_to_occupation_group(
        db_session, job=job, occupation_group_id=occupation_group_id
    )
    return IPostResponseBase[IOccupationGroupRead](
        message="Job added to occupation group", data=occupation_group
    )
