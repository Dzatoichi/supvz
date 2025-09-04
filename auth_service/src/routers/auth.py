from fastapi import APIRouter, Depends, status

from src.schemas.tokens import TokenResponse
from src.schemas.users_schemas import (
    PasswordResetConfirm,
    UserForgotPassword,
    UserLogin,
    UserRead,
    UserRegister,
)
from src.services.auth_service import AuthService
from src.utils.dependencies import get_auth_service_with_token, get_auth_service_without_token

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=UserRead)
async def register_user(
    user_in: UserRegister,
    auth_service: AuthService = Depends(get_auth_service_without_token),  # noqa: B008
):
    """Registration user."""
    user = await auth_service.register_user(user_in)

    return user


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service_with_token),  # noqa: B008
):
    """Authentication user."""
    user = await auth_service.login_user(credentials)

    return {"token": user.token}


@auth_router.post("/forgot_password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(
    data: UserForgotPassword,
    auth_service: AuthService = Depends(get_auth_service_without_token),  # noqa: B008
):
    """Route for func 'forgot_password'."""
    await auth_service.forgot_password(data.email)
    return {"detail": "If the email is registered, a reset link has been sent."}


@auth_router.post("/reset-password", responses={200: {"description": "Password successfully reset"}})
async def reset_password(
    confirm_data: PasswordResetConfirm,
    auth_service: AuthService = Depends(get_auth_service_with_token),  # noqa: B008
):
    """Reset user password."""

    result = await auth_service.reset_password(confirm_data.token, confirm_data.new_password)

    return result
