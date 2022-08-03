from typing import Dict, List, Union
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.schemas.role import IRoleCreate
from app.core.config import settings
from app.schemas.user import IUserCreate
from app.schemas.group import IGroupCreate
from app.schemas.occupation_group import IOccupationGroupCreate

roles: List[IRoleCreate] = [
    IRoleCreate(name="admin", description="This the Admin role"),
    IRoleCreate(name="manager", description="Manager role"),
    IRoleCreate(name="user", description="User role"),
]

groups: List[IGroupCreate] = [
    IGroupCreate(name="Sample Group", description="This is a sample group")
]

occupation_groups: List[IOccupationGroupCreate] = [
    IOccupationGroupCreate(name="Administration"),
    IOccupationGroupCreate(name="IT"),
    IOccupationGroupCreate(name="Marketing"),
    IOccupationGroupCreate(name="Human Resources"),
]

users: List[Dict[str, Union[str, IUserCreate]]] = [
    {
        "data": IUserCreate(
            first_name="Admin",
            last_name="Cool",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,
        ),
        "role": "admin",
    },
    {
        "data": IUserCreate(
            first_name="Manager",
            last_name="Cooler",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email="manager@example.com",
            is_superuser=False,
        ),
        "role": "manager",
    },
    {
        "data": IUserCreate(
            first_name="User",
            last_name="Coolest",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email="user@example.com",
            is_superuser=False,
        ),
        "role": "user",
    },
]


async def init_db(db_session: AsyncSession) -> None:

    for role in roles:
        role_current = await crud.role.get_role_by_name(db_session, name=role.name)
        if not role_current:
            await crud.role.create(db_session, obj_in=role)

    for user in users:
        current_user = await crud.user.get_by_email(
            db_session, email=user["data"].email
        )
        role = await crud.role.get_role_by_name(db_session, name=user["role"])
        if not current_user:
            user["data"].role_id = role.id
            await crud.user.create_with_role(db_session, obj_in=user["data"])

    for group in groups:
        current_group = await crud.group.get_group_by_name(db_session, name=group.name)
        if not current_group:
            new_group = await crud.group.create(db_session, obj_in=group)
            current_users = []
            for user in users:
                current_users.append(
                    await crud.user.get_by_email(db_session, email=user["data"].email)
                )
            await crud.group.add_users_to_group(
                db_session, users=current_users, group_id=new_group.id
            )

    for occupation_group in occupation_groups:
        current_occupation_group = (
            await crud.occupation_group.get_occupation_group_by_name(
                db_session, name=occupation_group.name
            )
        )
        if not current_occupation_group:
            new_group = await crud.occupation_group.create(
                db_session, obj_in=occupation_group
            )
