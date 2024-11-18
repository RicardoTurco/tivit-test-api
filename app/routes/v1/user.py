from fastapi import APIRouter, Response, status

from app.services.tivit_fake_service import TivitFakeService


user_router = APIRouter()

tag = "User"


@user_router.get(
    "/user",
    tags=[tag],
    summary="Retrieve user data",
    description="This endpoint retrieve user data."
)
async def get_user_data(username: str, response: Response):
    """
    Retrieve user data.

    :param username: name of user
    :param response: status code of request
    :return: data of user
    """
    tivit_fake_service = TivitFakeService()
    user_data = await tivit_fake_service.get_data_user(username)
    response.status_code = status.HTTP_200_OK
    return {"user_data": user_data}
