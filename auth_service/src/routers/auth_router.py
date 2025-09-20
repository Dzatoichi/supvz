from fastapi import APIRouter, Depends, Request, Response

from src.dao.tokensDAO import RefreshTokensDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.tokens import TokenSchema
from src.schemas.users_schemas import (
    PasswordResetConfirm,
    UserForgotPassword,
    UserLogin,
    UserLogout,
    UserRead,
    UserRegister,
)
from src.services.auth_service import AuthService
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.utils.dependencies import (
    get_auth_service,
    get_jwt_tokens_service,
    get_refresh_token_dao,
    get_stateful_token_service,
    get_users_dao,
)
from src.utils.rate_limiter import limiter

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=UserRead)
@limiter.limit("3/hour")
async def register_user(
    request: Request,
    user_in: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Registration user."""
    user = await auth_service.register_user(user_in, repo)

    return user


@auth_router.post("/login", response_model=TokenSchema)
@limiter.limit("5/minute")
async def login(
    request: Request,
    response: Response,
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
):
    """Authentication user."""
    access_token, refresh_token = await auth_service.login_user(
        credentials, repo, token_service
    )
    response.set_cookie(
        "refresh_token", refresh_token, httponly=True, max_age=3600 * 24 * 7
    )

    return {"access_token": access_token}


@auth_router.post(
    "/forgot_password",
    responses={
        200: {"description": "If the email is registered, a reset link has been sent"}
    },
)
@limiter.limit("5/hour")
async def forgot_password(
    request: Request,
    data: UserForgotPassword,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: StatefulTokenService = Depends(
        get_stateful_token_service
    ),  # noqa: B008
):
    """Route for func 'forgot_password'."""
    await auth_service.forgot_password(data.email, repo, token_service)


@auth_router.post(
    "/reset_password", responses={200: {"description": "Password successfully reset"}}
)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    confirm_data: PasswordResetConfirm,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: StatefulTokenService = Depends(
        get_stateful_token_service
    ),  # noqa: B008
):
    """Reset user password."""
    await auth_service.reset_password(
        confirm_data.token, confirm_data.new_password, token_service, repo
    )


@auth_router.post("/logout", response_model=dict, status_code=200)
async def logout(
    request: Request,
    response: Response,
    logout_data: UserLogout,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
):
    """Reset user password."""
    await auth_service.logout_user(
        refresh_token=logout_data.refresh_token,
        response=response,
        token_service=token_service,
    )
    return {"description": "Logged out successfully"}


@auth_router.post("/refresh_token", response_model=TokenSchema)
@limiter.limit("60/minute")
async def refresh_token(
    request: Request,
    refresh_token_in: str,
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
    repo: RefreshTokensDAO = Depends(get_refresh_token_dao),  # noqa: B008
):
    """Обновить refresh токен."""
    result = await token_service.refresh_token(
        refresh_token=refresh_token_in,
        repo=repo,
    )
    return result
