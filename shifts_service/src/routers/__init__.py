from fastapi import APIRouter

from src.routers.scheduled_shifts_router import scheduled_shifts_router

api_router = APIRouter()
api_router.include_router(scheduled_shifts_router)
