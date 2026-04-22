from fastapi import APIRouter

from .salary_rules_router import salary_rules_router
from .shift_penalties_router import penalties_router
from .shift_requests_router import shift_requests_router
from .shifts_router import shifts_router

from fastapi import APIRouter

from src.routers.scheduled_shifts_router import scheduled_shifts_router

api_router = APIRouter()
api_router.include_router(scheduled_shifts_router)

api_router.include_router(shifts_router)
api_router.include_router(penalties_router)
api_router.include_router(salary_rules_router)
api_router.include_router(shift_requests_router)
