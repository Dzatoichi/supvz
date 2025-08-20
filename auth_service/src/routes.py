from fastapi import APIRouter, Depends

from .dependencies import get_auth_service_without_token, get_auth_service_with_token
from .schemas import (
    TokenResponse,
    UserRegister, UserRead, UserLogin, UserPasswordUpdate,
)
from .service import AuthService

auth_router = APIRouter(prefix='/auth')


@auth_router.post("/register", response_model=UserRead)
async def register_user(
        user_in: UserRegister,
        auth_service: AuthService = Depends(get_auth_service_without_token),
):
    """Registration user."""
    user = await auth_service.register_user(user_in)

    return user


@auth_router.post("/login", response_model=TokenResponse)
async def login(
        credentials: UserLogin,
        auth_service: AuthService = Depends(get_auth_service_with_token)
):
    """Authentication user."""
    user = await auth_service.login_user(credentials)

    return {'token': user.token}


@auth_router.post("/{user_id}/reset-password")
async def reset_password(
        email: UserPasswordUpdate,
        auth_service: AuthService = Depends(get_auth_service_without_token),
):
    """Reset user password."""
    result = await auth_service.reset_password(email)

    return result
