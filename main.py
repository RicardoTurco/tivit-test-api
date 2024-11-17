from fastapi import FastAPI
from urls import router_v1


app = FastAPI(
    title="Tivit Test API",
    description="This is a simple test for python developer role"
)

app.include_router(router_v1, prefix="")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
