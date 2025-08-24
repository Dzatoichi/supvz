import asyncio

from auth_service.src.dao.users import UsersDAO
async def main():
    user_dao = UsersDAO()
    user = await user_dao.create({
        "email": "123",
        "phone_number": "123",
        "hashed_password": "123"
    })

    print(user)

if __name__ == "__main__":
    asyncio.run(main())
