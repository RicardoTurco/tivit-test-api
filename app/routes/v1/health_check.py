from fastapi import APIRouter, Response, status

from app.services.tivit_fake_service import TivitFakeService


health_router = APIRouter()

tag = "Health Check"


@health_router.get(
    "/external-health-check",
    tags=[tag],
    summary="Check status of external application",
    description="This endpoint returns a health check of external application.",
)
async def external_health_check(response: Response):
    """
    This endpoint returns a health check of external application.
    """
    health_check_external = await TivitFakeService.health_check()
    result = True if health_check_external else False
    response.status_code = status.HTTP_200_OK
    return {"external_application": result}


@health_router.get(
    "/health-check",
    tags=[tag],
    summary="Check status of application",
    description="This endpoint returns a health check of application.",
)
async def health_check(response: Response):
    """
    This endpoint returns a health check of application.
    """
    response.status_code = status.HTTP_200_OK
    return {"application": True}
