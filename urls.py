from fastapi.routing import APIRouter

from app.routes.v1 import admin, get_token, health_check, user

router_v1 = APIRouter(prefix="/v1")


router_v1.include_router(router=health_check.health_router)
router_v1.include_router(router=get_token.token_router)
router_v1.include_router(router=admin.admin_router)
router_v1.include_router(router=user.user_router)
