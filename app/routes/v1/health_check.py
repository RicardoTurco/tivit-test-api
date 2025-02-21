import logging

from fastapi import APIRouter, Response, status

from app.services.tivit_fake_service import TivitFakeService

logger = logging.getLogger(__name__)

health_router = APIRouter()

TAG = "Health Check"


@health_router.get(
    "/external-health-check",
    tags=[TAG],
    summary="Check status of external application",
    description="This endpoint returns a health check of external application.",
)
async def external_health_check(response: Response):
    """
    This endpoint returns a health check of external application.
    """
    logger.info("*** starting GET external-health-check endpoint")
    health_check_external = await TivitFakeService.external_health_check()
    result = bool(health_check_external)
    response.status_code = status.HTTP_200_OK
    logger.info("*** finishing GET external-health-check endpoint")
    return {"external_application": result}


@health_router.get(
    "/health-check",
    tags=[TAG],
    summary="Check status of application",
    description="This endpoint returns a health check of application.",
)
async def health_check(response: Response):
    """
    This endpoint returns a health check of application.
    """
    logger.info("*** starting GET health-check endpoint")
    response.status_code = status.HTTP_200_OK
    logger.info("*** finishing GET health-check endpoint")
    return {"application": True}
