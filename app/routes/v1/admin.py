import logging

from fastapi import APIRouter, Response, status

from app.decorators.decorators import check_external_service_health
from app.services.tivit_fake_service import TivitFakeService

logger = logging.getLogger(__name__)

admin_router = APIRouter()

tag = "Admin"


@admin_router.get(
    "/admin",
    tags=[tag],
    summary="Retrieve admin data",
    description="This endpoint retrieve admin data",
)
@check_external_service_health()
async def get_admin_data(username: str, response: Response):
    """
    Retrieve admin data.

    :param username: name of admin user
    :param response: status code of request
    :return: data of admin
    """
    logger.info("*** starting GET admin endpoint")
    tivit_fake_service = TivitFakeService()
    admin_data = await tivit_fake_service.get_data_admin(username)
    response.status_code = status.HTTP_200_OK
    logger.info("*** finishing GET admin endpoint")
    return {"admin_data": admin_data}
