from fastapi import APIRouter

from .employees_router import employees_router
from .pvz_group_router import pvz_groups_router
from .pvz_router import pvz_router

api_router = APIRouter()

api_router.include_router(pvz_router)
api_router.include_router(pvz_groups_router)
api_router.include_router(employees_router)
