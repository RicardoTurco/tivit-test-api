from fastapi import APIRouter, Response, status


health_router = APIRouter()

tag = "Health Check"


@health_router.get("/health-check", tags=[tag], summary="Check status of application")
async def health_check(response: Response):
    """
    This endpoint returns a health check of application.
    """
    response.status_code = status.HTTP_200_OK
    return {"application": True}
