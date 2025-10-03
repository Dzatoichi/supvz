from fastapi import APIRouter, Depends, Request, Response

from src.dao.usersDAO import UsersDAO
from src.schemas.tokens_schemas import TokenSchema
from src.schemas.users_schemas import (
    PasswordResetConfirmSchema,
    UserForgotPasswordSchema,
    UserLoginSchema,
    UserLogoutSchema,
    UserReadSchema,
    UserRegisterSchema,
)
from src.services.auth_service import AuthService
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.utils.dependencies import (
    get_auth_service,
    get_jwt_tokens_service,
    get_stateful_token_service,
    get_users_dao,
)
from src.utils.rate_limiter import limiter

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=UserReadSchema)
@limiter.limit("3/hour")
async def register_user(
    request: Request,
    user_in: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """
    Ручка регистрации пользователя.
    POST [/auth/register]
    """
    user = await auth_service.register_user(user_in, repo)

    return user


@auth_router.post("/login", response_model=dict, status_code=200)
@limiter.limit("5/minute")
async def login(
    request: Request,
    response: Response,
    credentials: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
):
    """
    Ручка аутентификации пользователя.
    POST [/auth/login]
    """
    access_token, refresh_token = await auth_service.login_user(credentials, repo, token_service)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        max_age=3600 * 1,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        max_age=3600 * 24 * 7,
    )

    return {"description": "Log In successfully"}


@auth_router.post(
    "/forgot_password",
    responses={200: {"description": "If the email is registered, a reset link has been sent"}},
)
@limiter.limit("5/hour")
async def forgot_password(
    request: Request,
    data: UserForgotPasswordSchema,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: StatefulTokenService = Depends(  # noqa: B008
        get_stateful_token_service
    ),
):
    """
    Ручка запроса на изменение-сброс пароля пользователя в случае, если пользователь забыл пароль.
    POST [/auth/forgot_password]
    """
    await auth_service.forgot_password(data.email, repo, token_service)


@auth_router.post("/reset_password", responses={200: {"description": "Password successfully reset"}})
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    confirm_data: PasswordResetConfirmSchema,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: StatefulTokenService = Depends(  # noqa: B008
        get_stateful_token_service
    ),
):
    """
    Ручка сброса пароля.
    POST [/auth/reset_password]
    """
    await auth_service.reset_password(confirm_data.token, confirm_data.new_password, token_service, repo)


@limiter.limit("5/minute")
@auth_router.post("/logout", response_model=dict, status_code=200)
async def logout(
    request: Request,
    response: Response,
    logout_data: UserLogoutSchema,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
):
    """
    Ручка завершения сессии/выхода пользователя.
    POST [/auth/logout]
    """
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
    response: Response,
    refresh_token_in: str,
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
):
    """
    Ручка для обновления access-токена, выдачи нового refresh-токена.
    POST [/auth/refresh_token]
    """
    result = await token_service.refresh_token(refresh_token=refresh_token_in)
    refresh_token = result["refresh_token"]

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        max_age=3600 * 24 * 7,
    )

    return result
