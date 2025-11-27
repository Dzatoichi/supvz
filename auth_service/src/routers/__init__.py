from fastapi import APIRouter

from .auth_router import auth_router
from .positions_router import positions_router
from .users_router import users_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(positions_router)
