from fastapi import HTTPException, status
from functools import wraps

from app.services.tivit_fake_service import TivitFakeService


def check_external_service_health():
    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            external_health_check = await TivitFakeService.health_check()
            if not external_health_check:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="External application is not ok",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
