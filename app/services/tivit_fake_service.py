import requests

from fastapi import HTTPException

from app.schemas.token import TokenCredentials, TokenSchema
from app.constants.constants import URL_TIVIT_TOKEN


class TivitFakeService:

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
                raise HTTPException(status_code=500, detail="Token not found in response")

            return {"access_token": token_data.get("access_token"), "token_type": token_data.get("token_type")}

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error to obtain token: {e}")
