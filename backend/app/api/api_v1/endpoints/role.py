from app.models.user import User
from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.role import IRoleCreate, IRoleRead, IRoleUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app import crud
from uuid import UUID
from app.schemas.role import IRoleEnum

router = APIRouter()    

@router.get("/role", response_model=IGetResponseBase[Page[IRoleRead]])
async def get_roles(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    roles = await crud.role.get_multi_paginated(db_session, params=params)
    return IGetResponseBase[Page[IRoleRead]](data=roles)

@router.get("/role/{role_id}", response_model=IGetResponseBase[IRoleRead])
async def get_role_by_id(
    role_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    role = await crud.role.get(db_session, id=role_id)
    return IGetResponseBase[IRoleRead](data=role)

@router.post("/role", response_model=IPostResponseBase[IRoleRead])
async def create_role(
    role: IRoleCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin])),
):
    new_permission = await crud.role.create(db_session, obj_in=role)
    return IPostResponseBase[IRoleRead](data=new_permission)  

@router.put("/role/{role_id}", response_model=IPutResponseBase[IRoleRead])
async def update_permission(
    role_id: UUID,
    role: IRoleUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin])),
):
    current_role = await crud.role.get(db_session=db_session, id=role_id)
    if not current_role:
        raise HTTPException(status_code=404, detail="Permission not found")

    updated_role = await crud.role.update(db_session, obj_current=current_role, obj_new=role)
    return IPutResponseBase[IRoleRead](data=updated_role)  

