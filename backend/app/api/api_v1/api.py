from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    user,
    login,
    role,
    group,
    job,
    occupation_group,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login_form"])
api_router.include_router(role.router, tags=["role"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(group.router, tags=["group"])
api_router.include_router(job.router, tags=["job"])
api_router.include_router(occupation_group.router, tags=["occupation_group"])
