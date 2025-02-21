import logging

from app.constants.constants import FAKE_USERS_DB

logger = logging.getLogger(__name__)


class FakeUserDb:
    """
    Class Fake user DB
    """

    @staticmethod
    async def get_fake_users_db() -> dict:
        """
        Get all users from 'fake' DB.
        """
        return FAKE_USERS_DB

    @staticmethod
    async def get_fake_user_by_name(username: str) -> dict:
        """
        Get 'fake' user from DB by name.

        :param username: user to find
        :return: user 'fake' from DB
        """
        logger.info("*** function: get_fake_user_by_name")
        user_db = FAKE_USERS_DB.get(username, {})
        return user_db

    @staticmethod
    async def user_is_admin(username: str) -> bool:
        """
        Check if user is 'admin'.

        :param username: user to check
        :return: True / False
        """
        user_db = FAKE_USERS_DB.get(username, {})
        result = bool(user_db and user_db.get("role") == "admin")
        return result

    @staticmethod
    async def user_is_user(username: str) -> bool:
        """
        Check if user is 'user'.

        :param username: user to check
        :return: True / False
        """
        user_db = FAKE_USERS_DB.get(username, {})
        result = bool(user_db and user_db.get("role") == "user")
        return result
