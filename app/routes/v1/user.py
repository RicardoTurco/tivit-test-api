import logging
from fastapi import APIRouter, Response, status

from app.decorators.decorators import check_external_service_health
from app.services.tivit_fake_service import TivitFakeService

logger = logging.getLogger(__name__)

user_router = APIRouter()

tag = "User"


@user_router.get(
    "/user",
    tags=[tag],
    summary="Retrieve user data",
    description="This endpoint retrieve user data.",
)
@check_external_service_health()
async def get_user_data(username: str, response: Response):
    """
    Retrieve user data.

    :param username: name of user
    :param response: status code of request
    :return: data of user
    """
    logger.info("*** starting GET user endpoint")
    tivit_fake_service = TivitFakeService()
    user_data = await tivit_fake_service.get_data_user(username)
    response.status_code = status.HTTP_200_OK
    logger.info("*** finishing GET user endpoint")
    return {"user_data": user_data}
