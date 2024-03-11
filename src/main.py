# import logging

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse  # , Request, Response
# from starlette.types import Message
# from starlette.background import BackgroundTask

from src.ctrm.database.db import init_db
from src.ctrm.config.settings import get_settings
from src.ctrm.api.v1.api import api_router
from src.ctrm.services.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=get_settings().PROJECT_NAME,
        on_startup=[init_db],
        openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
    )

    app.include_router(api_router, prefix=get_settings().API_V1_STR)

    app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

    return app


app = create_app()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8080)
