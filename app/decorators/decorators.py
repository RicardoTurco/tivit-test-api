import logging
from functools import wraps

from fastapi import HTTPException, status

from app.services.tivit_fake_service import TivitFakeService

logger = logging.getLogger(__name__)


def check_external_service_health():
    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info("*** starting decorator: check_external_service_health")

            external_health_check = await TivitFakeService.external_health_check()
            if not external_health_check:
                logger.critical("External application is not ok")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="External application is not ok",
                )

            logger.info("*** finishing decorator: check_external_service_health")
            return await func(*args, **kwargs)

        return wrapper

    return decorator
