from fastapi import Response


class FakeUsersDAO:
    pass


class FakeAuthService:
    async def register_user(self, user_in, repo):
        return {
            "id": 1,
            "email": user_in.email,
            "name": user_in.name,
            "role": "owner",
            "created_at": "2024-01-01T00:00:00",
        }

    async def login_user(self, credentials, repo, token_service):
        return {"access_token": "access_token", "refresh_token": "refresh_token"}

    async def forgot_password(self, email, repo, token_service):
        return None

    async def reset_password(self, token, new_password, token_service, repo):
        return None

    async def logout_user(
        self,
        refresh_token: str,
        response: Response,
        token_service,
    ):
        return {"description": "Logged out successfully"}


class FakeJWTTokensService:
    async def refresh_token(self, refresh_token):
        return {"refresh_token": "refresh", "access_token": "access"}


class FakeStatefulTokenService:
    pass
