from fastapi import APIRouter, Depends, status, exceptions, HTTPException

from .dependencies import get_auth_service_without_token, get_auth_service_with_token
from .schemas import (
    TokenResponse,
    UserRegister, UserRead, UserLogin, UserPasswordUpdate, UserForgotPassword, PasswordResetConfirm,
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


@auth_router.post('/forgot_password', status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(
        data: UserForgotPassword,
        auth_service: AuthService = Depends(get_auth_service_without_token),
):
    """Route for func 'forgot_password'."""
    user = await auth_service.get_by_email(data.email)

    if user:
        return await auth_service.forgot_password(user)


@auth_router.post(
    "/reset-password",
    responses={200: {"description": "Password successfully reset"}}
)
async def reset_password(
        confirm_data: PasswordResetConfirm,
        auth_service: AuthService = Depends(get_auth_service_with_token),
):
    """Reset user password."""

    result = await auth_service.reset_password(confirm_data.token, confirm_data.new_password)

    return result
