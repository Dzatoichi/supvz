from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Request, Response

from src.dao.tokensDAO import RefreshTokensDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import (
    PasswordResetConfirmSchema,
    UserAuthRequestSchema,
    UserAuthResponseSchema,
    UserForgotPasswordSchema,
    UserLoginSchema,
    UserReadSchema,
    UserRegisterSchema,
    UserRegisterEmployeeSchema,
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

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserReadSchema)
@limiter.limit("3/hour")
async def register_user(
    request: Request,
    user_in: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
):
    """
    Ручка регистрации пользователя.
    POST [/auth/register]
    """
    user = await auth_service.register_user(data=user_in, repo=repo)

    return user


@auth_router.post("/login", response_model=dict, status_code=200)
@limiter.limit("5/minute")
async def login(
    request: Request,
    response: Response,
    credentials: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
):
    """
    Ручка аутентификации пользователя.
    POST [/auth/login]
    """
    access_token, refresh_token = await auth_service.login_user(
        credentials=credentials,
        repo=repo,
        token_service=token_service,
    )

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
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: StatefulTokenService = Depends(get_stateful_token_service),
):
    """
    Ручка запроса на изменение-сброс пароля пользователя в случае, если пользователь забыл пароль.
    POST [/auth/forgot_password]
    """
    await auth_service.forgot_password(
        user_email=data.email,
        repo=repo,
        token_service=token_service,
    )


@auth_router.post("/reset_password", responses={200: {"description": "Password successfully reset"}})
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    confirm_data: PasswordResetConfirmSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: StatefulTokenService = Depends(get_stateful_token_service),
):
    """
    Ручка сброса пароля.
    POST [/auth/reset_password]
    """
    await auth_service.reset_password(
        token=confirm_data.token,
        new_password=confirm_data.new_password,
        token_service=token_service,
        repo=repo,
    )


@limiter.limit("5/minute")
@auth_router.post("/logout", response_model=dict, status_code=200)
async def logout(
    request: Request,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    auth_service: AuthService = Depends(get_auth_service),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
):
    """
    Ручка завершения сессии/выхода пользователя.
    POST [/auth/logout]
    """
    await auth_service.logout_user(refresh_token=refresh_token, response=response, token_service=token_service)
    return {"description": "Logged out successfully"}


@auth_router.post("/refresh_token", response_model=dict, status_code=200)
@limiter.limit("60/minute")
async def refresh_token(
    request: Request,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
    repo: RefreshTokensDAO = Depends(get_refresh_token_dao),
):
    """
    Ручка для обновления access-токена, выдачи нового refresh-токена.
    POST [/auth/refresh_token]
    """
    result = await token_service.refresh_token(refresh_token=refresh_token, repo=repo)
    refresh_token = result["refresh_token"]
    access_token = result["access_token"]

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

    return {"description": "Refreshed successfully"}


@auth_router.post("/authorize")
async def authorize_user(
    request: Request,
    permission: str,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
    token_repo: RefreshTokensDAO = Depends(get_refresh_token_dao),
):
    """
    Авторизация пользователя по access токену.
    """
    token = request.cookies.get("access_token")
    await auth_service.authorize_user(
        token=token,
        token_service=token_service,
        repo=repo,
        token_repo=token_repo,
        permission=permission,
    )

    return

@auth_router.post("/generate_register_token", response_model=dict)
async def generate_register_token(
        request: Request,
        employee_data: UserRegisterEmployeeSchema,
        auth_service: AuthService = Depends(get_auth_service),
        token_service: JWTTokensService = Depends(get_jwt_tokens_service),
):
    """
    Создание токена регистрации сотрудника
    """
    result = await auth_service.generate_register_token(
        employee_data=employee_data,
        token_service=token_service,
    )
    return result