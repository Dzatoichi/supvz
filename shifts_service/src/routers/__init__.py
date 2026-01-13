from fastapi import APIRouter

from .shift_penalties_router import shift_penalties_router
from .shifts_router import shifts_router

api_router = APIRouter()

api_router.include_router(shifts_router)
api_router.include_router(shift_penalties_router)
