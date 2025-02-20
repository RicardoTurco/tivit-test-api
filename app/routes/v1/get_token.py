import logging

from fastapi import APIRouter, Response, status

from app.decorators.decorators import check_external_service_health
from app.schemas.token import TokenCredentials
from app.services.tivit_fake_service import TivitFakeService

logger = logging.getLogger(__name__)

token_router = APIRouter()

tag = "Token"


@token_router.post(
    "/get-token",
    tags=[tag],
    summary="Retrieve token to use for endpoints.",
    description="This endpoint retrieve token to use for endpoints.",
)
@check_external_service_health()
async def get_token(token_credentials: TokenCredentials, response: Response):
    """
    Retrieve token to use for endpoints.

    :param token_credentials: credentials for user to retrieve token
    :param response: status code of request
    :return: token and type of token
    """
    logger.info("*** starting GET token endpoint")
    tivit_fake_service = TivitFakeService()
    token_data = await tivit_fake_service.get_token(
        credentials=token_credentials,
        user_db={},
        find_in_db=True,
    )
    response.status_code = status.HTTP_200_OK
    logger.info("*** finishing GET token endpoint")
    return {
        "access_token": token_data.get("access_token"),
        "token_type": token_data.get("token_type"),
    }
