import logging

from fastapi import HTTPException, status

from app.core.singleton_meta import SingletonMeta
from app.repositories.fake_user_repository import FakeUserDb

logger = logging.getLogger(__name__)


class UserFromDb(metaclass=SingletonMeta):

    @staticmethod
    async def find_user_db(username: str, not_found_msg: str):
        logger.info("*** function: find_user_db")

        fake_user_db = FakeUserDb()
        any_user_db = await fake_user_db.get_fake_user_by_name(username)

        msg_not_found = (
            "User admin not found" if not_found_msg == "admin" else "User not found"
        )
        if not any_user_db:
            logger.warning(f"*** {username} - {msg_not_found} !")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=msg_not_found
            )

        return any_user_db

    @staticmethod
    async def check_user_role(any_user_db: dict, role: str):
        logger.info("*** function: check_user_role")

        if any_user_db.get("role") != role:
            logger.warning(f" *** Role {role} is insufficient")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized"
            )
