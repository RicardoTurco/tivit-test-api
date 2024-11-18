import requests

from fastapi import HTTPException, status

from app.constants.constants import (
    URL_TIVIT_HEALTH, URL_TIVIT_TOKEN, URL_TIVIT_ADMIN, URL_TIVIT_USER
)
from app.repositories.fake_user_repository import FakeUserDb
from app.schemas.token import TokenCredentials


class TivitFakeService:

    @staticmethod
    async def health_check() -> bool:
        """
        Verify a health check of external application.

        :return: True / False
        """
        try:
            response = requests.get(URL_TIVIT_HEALTH, verify=False)
            response.raise_for_status()
            health_check_data = response.json()

            result = True if response.status_code == status.HTTP_200_OK and health_check_data.get("status") == "ok" else False

            return result

        except HTTPException as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error to verify health check of external application {e}")

    @staticmethod
    async def get_token(credentials: TokenCredentials):
        """
        Retrieve access_token of a user.

        :param credentials: Credentials pass in request body
        :return: access_token of a user
        """
        params = {
            "username": credentials.username,
            "password": credentials.password
        }

        try:
            response = requests.post(
                URL_TIVIT_TOKEN,
                params=params,
                verify=False
            )
            response.raise_for_status()
            token_data = response.json()

            if "access_token" not in token_data:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Token not found in response")

            return {"access_token": token_data.get("access_token"), "token_type": token_data.get("token_type")}

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code,
                                detail=f"Error to obtain token: {e.detail}")

    @staticmethod
    async def admin_data_external(username: str) -> dict:
        """
        Retrieve admin data from api external

        :param username: name of admin
        :return: data of admin
        """
        fake_user_db = FakeUserDb()

        user_db = await fake_user_db.get_fake_user_by_name(username)
        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User admin not found")

        if not user_db.get("role") == "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User not authorized")

        user_credentials = TokenCredentials(username=user_db.get("username"),
                                            password=user_db.get("password"))
        user_token = await TivitFakeService.get_token(user_credentials)
        headers = {"Authorization": f"Bearer {user_token.get("access_token")}"}

        response = requests.get(URL_TIVIT_ADMIN,
                                headers=headers,
                                verify=False)
        admin_data_external = response.json()

        return admin_data_external

    @staticmethod
    async def get_data_admin(username: str) -> dict:
        """
        Calls external api to retrieve admin data.

        :param username: name of admin
        :return: data of admin
        """
        try:
            admin_data_external = await TivitFakeService.admin_data_external(username)
            return admin_data_external
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code,
                                detail=f"Error to obtain admin information: {e.detail}")

    @staticmethod
    async def user_data_external(username: str) -> dict:
        """
        Retrieve user data from api external

        :param username: name of user
        :return: data of user
        """
        fake_user_db = FakeUserDb()

        user_db = await fake_user_db.get_fake_user_by_name(username)
        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if not user_db.get("role") == "user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User not authorized")

        user_credentials = TokenCredentials(username=user_db.get("username"),
                                            password=user_db.get("password"))
        user_token = await TivitFakeService.get_token(user_credentials)
        headers = {"Authorization": f"Bearer {user_token.get("access_token")}"}

        response = requests.get(URL_TIVIT_USER,
                                headers=headers,
                                verify=False)
        user_data_external = response.json()

        return user_data_external

    @staticmethod
    async def get_data_user(username: str) -> dict:
        """
        Calls external api to retrieve user data.

        :param username: name of user
        :return: data of user
        """
        try:
            user_data_external = await TivitFakeService.user_data_external(username)
            return user_data_external
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code,
                                detail=f"Error to obtain admin information: {e.detail}")
