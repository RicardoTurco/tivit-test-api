from fastapi import APIRouter, Response, status

from app.services.tivit_fake_service import TivitFakeService


admin_router = APIRouter()

tag = "Admin"


@admin_router.get(
    "/admin",
    tags=[tag],
    summary="Retrieve admin data",
    description="This endpoint retrieve admin data"
)
async def get_admin_data(username: str, response: Response):
    """
    Retrieve admin data.

    :param username: name of admin user
    :param response: status code of request
    :return: data of admin
    """
    tivit_fake_service = TivitFakeService()
    admin_data = await tivit_fake_service.get_data_admin(username)
    response.status_code = status.HTTP_200_OK
    return {"admin_data": admin_data}
