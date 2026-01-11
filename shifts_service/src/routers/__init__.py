from fastapi import APIRouter

from .shifts_router import shifts_router

api_router = APIRouter()

api_router.include_router(shifts_router)
