from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from urls import router_v1


def get_app() -> FastAPI:
    app = FastAPI(
        title="Tivit Test API",
        description="This is a simple test for python developer role",
    )

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router_v1, prefix="")

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:get_app",
        host="0.0.0.0",
        port=8081,
        log_config="log_conf.yaml",
        factory=True,
    )
