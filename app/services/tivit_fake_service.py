import requests

from fastapi import HTTPException, status

from app.schemas.token import TokenCredentials, TokenSchema
from app.constants.constants import URL_TIVIT_HEALTH, URL_TIVIT_TOKEN


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

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error to verify health check of external application {e}")

    @staticmethod
    async def get_token(credentials: TokenCredentials):
        """
        Retrieve access_token of a user.

        :param credentials: Credentials pass in request body
        :return: access_token of a user
        """
        external_health_check = await TivitFakeService.health_check()
        if not external_health_check:
            raise HTTPException(status_code=500, detail="External application is not ok")

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
                raise HTTPException(status_code=500, detail="Token not found in response")

            return {"access_token": token_data.get("access_token"), "token_type": token_data.get("token_type")}

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error to obtain token: {e}")
