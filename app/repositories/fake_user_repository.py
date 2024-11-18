from app.constants.constants import FAKE_USERS_DB


class FakeUserDb:

    @staticmethod
    async def get_fake_users_db() -> dict:
        return FAKE_USERS_DB

    @staticmethod
    async def get_fake_user_by_name(username: str) -> dict:
        user_db = FAKE_USERS_DB.get(username, {})
        return user_db

    @staticmethod
    async def user_is_admin(username: str) -> bool:
        user_db = FAKE_USERS_DB.get(username, {})
        result = True if user_db and user_db.get("role") == "admin" else False
        return result

    @staticmethod
    async def user_is_user(username: str) -> bool:
        user_db = FAKE_USERS_DB.get(username, {})
        result = True if user_db and user_db.get("role") == "user" else False
        return result
