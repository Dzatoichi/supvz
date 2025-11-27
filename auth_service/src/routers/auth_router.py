from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Request, Response

from src.core.security.permissions import PermissionEnum
from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import (
    PasswordResetConfirmSchema,
    UserForgotPasswordSchema,
    UserLoginSchema,
    UserReadSchema,
    UserRegisterEmployeeSchema,
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

auth_router = APIRouter(prefix="/auth", tags=["Authorization"])


@auth_router.post("/register", response_model=UserReadSchema, status_code=201)
async def register_user(
    user_in: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: JWTTokensService | None = Depends(get_jwt_tokens_service),
) -> UserReadSchema:
    """
    Ручка регистрации пользователя.
    POST [/auth/register]
    """
    if user_in.register_token:
        user = await auth_service.register_user(
            data=user_in,
            repo=repo,
            token_service=token_service,
        )
        return user

    user = await auth_service.register_user(
        data=user_in,
        repo=repo,
        token_service=None,
    )

    return user


@auth_router.post("/login", responses={200: {"description": "Succesful login"}})
async def login(
    response: Response,
    credentials: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
) -> None:
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


@auth_router.post(
    "/forgot_password",
    responses={200: {"description": "If the email is registered, a reset link has been sent"}},
)
async def forgot_password(
    data: UserForgotPasswordSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: StatefulTokenService = Depends(get_stateful_token_service),
) -> None:
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
async def reset_password(
    confirm_data: PasswordResetConfirmSchema,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: StatefulTokenService = Depends(get_stateful_token_service),
) -> None:
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


@auth_router.post("/logout", responses={200: {"description": "Logged out successfully"}})
async def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    auth_service: AuthService = Depends(get_auth_service),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
) -> None:
    """
    Ручка завершения сессии/выхода пользователя.
    POST [/auth/logout]
    """
    await auth_service.logout_user(refresh_token=refresh_token, response=response, token_service=token_service)


@auth_router.post("/refresh_token", responses={200: {"description": "Refreshed successfully"}})
async def refresh_token(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
) -> None:
    """
    Ручка для обновления access-токена, выдачи нового refresh-токена.
    POST [/auth/refresh_token]
    """
    result = await token_service.refresh_token(refresh_token=refresh_token)
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


@auth_router.post("/authorize", status_code=200)
async def authorize_user(
    request: Request,
    permission: PermissionEnum,
    auth_service: AuthService = Depends(get_auth_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
) -> None:
    """
    Авторизация пользователя по access токену.
    """
    token = request.cookies.get("access_token")
    await auth_service.authorize_user(
        token=token,
        token_service=token_service,
        repo=repo,
        permission=permission,
    )

    return


@auth_router.post("/generate_register_token", response_model=dict)
async def generate_register_token(
    employee_data: UserRegisterEmployeeSchema,
    auth_service: AuthService = Depends(get_auth_service),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
    repo: UsersDAO = Depends(get_users_dao),
):
    """
    Создание токена регистрации сотрудника
    """
    result = await auth_service.generate_register_token(
        employee_data=employee_data,
        token_service=token_service,
        repo=repo,
    )
    return result
