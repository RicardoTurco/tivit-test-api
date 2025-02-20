import logging

import requests
from fastapi import HTTPException, status

from app.constants.constants import (
    URL_TIVIT_ADMIN,
    URL_TIVIT_HEALTH,
    URL_TIVIT_TOKEN,
    URL_TIVIT_USER,
)
from app.schemas.token import TokenCredentials
from app.utils.utils import UserFromDb

logger = logging.getLogger(__name__)


class TivitFakeService:
    """
    Class Tivit fake service
    """

    @staticmethod
    async def external_health_check() -> bool:
        """
        Verify a health check of external application.

        :return: True / False
        """
        logger.info("*** function: external_health_check")
        try:
            logger.info("*** Call external application: GET %s", URL_TIVIT_HEALTH)
            response = requests.get(URL_TIVIT_HEALTH, verify=False, timeout=30)
            response.raise_for_status()
            health_check_data = response.json()

            result = bool(
                response.status_code == status.HTTP_200_OK
                and health_check_data.get("status") == "ok"
            )

            return result

        except HTTPException as e:
            logger.warning(
                "*** Error to verify health check of external application %s", e
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error to verify health check of external application {e}",
            ) from e

    @staticmethod
    async def get_token(credentials: TokenCredentials, user_db: dict, find_in_db: bool):
        """
        Retrieve access_token of a user.

        :param credentials: Credentials pass in request body
        :param user_db: information of user from db
        :param find_in_db: find user in DB ?
        :return: access_token of a user
        """
        logger.info("*** function: get_token")
        try:
            if find_in_db:
                user_from_db = UserFromDb()

                any_user_db = await user_from_db.find_user_db(
                    username=credentials.username, not_found_msg=credentials.username
                )
            else:
                any_user_db = user_db

            if credentials.password != any_user_db.get("password"):
                logger.warning(
                    "*** Wrong password for user: %s", any_user_db.get("username")
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Wrong password",
                )

            params = {
                "username": any_user_db.get("username"),
                "password": any_user_db.get("password"),
            }

            logger.info("*** Call external application: POST %s", URL_TIVIT_TOKEN)
            response = requests.post(
                URL_TIVIT_TOKEN, params=params, verify=False, timeout=30
            )
            response.raise_for_status()
            token_data = response.json()

            if "access_token" not in token_data:
                logger.warning("*** Token not found in response. Params: %s", params)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token not found in response",
                )

            return {
                "access_token": token_data.get("access_token"),
                "token_type": token_data.get("token_type"),
            }

        except HTTPException as e:
            logger.warning("*** Error to obtain token: %s", e.detail)
            raise HTTPException(
                status_code=e.status_code, detail=f"Error to obtain token: {e.detail}"
            ) from e

    @staticmethod
    async def data_external_user_info(
        username: str, not_found_msg: str, role: str, url_tivit: str
    ) -> dict:
        """
        Retrieve data from api external

        :param username: name of any user
        :param not_found_msg: who's to destination msg when user not found
        :param role: role of user
        :param url_tivit: url to external tivit service
        :return: data returned
        """
        logger.info("*** function: data_external_user_info")

        user_from_db = UserFromDb()

        any_user_db = await user_from_db.find_user_db(
            username=username, not_found_msg=not_found_msg
        )

        await user_from_db.check_user_role(any_user_db=any_user_db, role=role)

        user_credentials = TokenCredentials(
            username=any_user_db.get("username"), password=any_user_db.get("password")
        )
        user_token = await TivitFakeService.get_token(
            credentials=user_credentials,
            user_db=any_user_db,
            find_in_db=False,
        )
        headers = {"Authorization": f"Bearer {user_token.get("access_token")}"}

        logger.info("*** Call external application: GET %s", url_tivit)
        response = requests.get(url_tivit, headers=headers, verify=False, timeout=30)

        return response.json()

    @staticmethod
    async def get_data_admin(username: str) -> dict:
        """
        Calls external api to retrieve admin data.

        :param username: name of admin
        :return: data of admin
        """
        logger.info("*** function: get_data_admin")
        try:
            admin_data_external = await TivitFakeService.data_external_user_info(
                username=username,
                not_found_msg="admin",
                role="admin",
                url_tivit=URL_TIVIT_ADMIN,
            )
            return admin_data_external
        except HTTPException as e:
            logger.warning("*** Error to obtain admin information: %s", e.detail)
            raise HTTPException(
                status_code=e.status_code,
                detail=f"Error to obtain admin information: {e.detail}",
            ) from e

    @staticmethod
    async def get_data_user(username: str) -> dict:
        """
        Calls external api to retrieve user data.

        :param username: name of user
        :return: data of user
        """
        logger.info("*** function: get_data_user")
        try:
            user_data_external = await TivitFakeService.data_external_user_info(
                username=username,
                not_found_msg="user",
                role="user",
                url_tivit=URL_TIVIT_USER,
            )
            return user_data_external
        except HTTPException as e:
            logger.warning("*** Error to obtain user information: %s", e.detail)
            raise HTTPException(
                status_code=e.status_code,
                detail=f"Error to obtain user information: {e.detail}",
            ) from e
