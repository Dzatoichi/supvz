import asyncio

from auth_service.src.dao.usersDAO import UsersDAO  # Импорт твоего DAO


async def main():
    user_dao = UsersDAO()

    # Тест get_by_id
    user = await user_dao.get_by_id(1)
    print(f"User by ID: {user}")

    try:
        await user_dao.get_user_by_email(user.email + "123")
    except Exception as e:
        print(f"Expected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
