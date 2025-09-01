from fastapi import FastAPI
import asyncio
from auth_service.src.dao.usersDAO import UsersDAO

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Auth Service Running!"}

async def main():
    user_dao = UsersDAO()
    user = await user_dao.get_by_id(1)
    print(await user_dao.get_user_by_email(user.email+"123"))

if __name__ == "__main__":
    asyncio.run(main())
