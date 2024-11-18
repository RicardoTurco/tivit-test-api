from fastapi import APIRouter, Response, status

from app.schemas.token import TokenCredentials
from app.services.tivit_fake_service import TivitFakeService


token_router = APIRouter()

tag = "Token"


@token_router.post("/get-token", tags=[tag], summary="Retrieve token to use")
async def get_token(token_credentials: TokenCredentials, response: Response):
    tivit_fake_service = TivitFakeService()
    token_data = await tivit_fake_service.get_token(token_credentials)
    response.status_code = status.HTTP_200_OK
    return {"access_token": token_data.get("access_token"), "token_type": token_data.get("token_type")}
