import logging

from fastapi import HTTPException, status

from app.core.singleton_meta import SingletonMeta
from app.repositories.fake_user_repository import FakeUserDb

logger = logging.getLogger(__name__)


class UserFromDb(metaclass=SingletonMeta):
    """
    Class User from DB.
    """

    @staticmethod
    async def find_user_db(username: str, not_found_msg: str):
        """
        Find user in DB.

        :param username: name of user to find
        :param not_found_msg: type of user to show message if not find id
        :return: user from DB
        """
        logger.info("*** function: find_user_db")

        fake_user_db = FakeUserDb()
        any_user_db = await fake_user_db.get_fake_user_by_name(username)

        msg_not_found = (
            "User admin not found" if not_found_msg == "admin" else "User not found"
        )
        if not any_user_db:
            logger.warning("*** %s - %s !", username, msg_not_found)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=msg_not_found
            )

        return any_user_db

    @staticmethod
    async def check_user_role(any_user_db: dict, role: str):
        """
        Check if role of user from DB is equal to role informed.
        If isn't equal, dispatch a raise exception.

        :param any_user_db: user from DB
        :param role: role to compare
        """
        logger.info("*** function: check_user_role")

        if any_user_db.get("role") != role:
            logger.critical(
                " *** The role: %s of user: %s, is insufficient.",
                any_user_db.get("role"),
                any_user_db.get("username"),
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized"
            )
