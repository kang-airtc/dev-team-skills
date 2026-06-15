from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.logging import configure_logging
from server.settings import settings
from server.web.api.router import api_router
from server.web.app_events import register_shutdown_event, register_startup_event

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application
    """
    configure_logging()
    app = FastAPI(
        title="company-site",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # 静态文件：用户上传的图片
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    app.mount(
        settings.upload_url_prefix,
        StaticFiles(directory=str(settings.upload_dir)),
        name="uploads",
    )

    # CORS：浏览器规范禁止 allow_origins=["*"] 与 allow_credentials=True 同时使用
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
