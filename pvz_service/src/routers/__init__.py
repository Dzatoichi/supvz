from fastapi import APIRouter

from .pvz_router import pvz_router
api_router = APIRouter()

api_router.include_router(pvz_router)
