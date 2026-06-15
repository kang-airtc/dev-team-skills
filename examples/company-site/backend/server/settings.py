# server/settings.py

import enum
import os
from pathlib import Path
from tempfile import gettempdir
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

BASE_DIR = Path(__file__).parent

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False

    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "server"
    db_pass: str = "server"
    db_base: str = "server"
    db_echo: bool = False

    # 文件上传：写入到 backend/uploads/，并通过 /uploads 静态路径对外暴露
    upload_dir: Path = BASE_DIR.parent / "uploads"
    upload_url_prefix: str = "/uploads"
    upload_max_bytes: int = 5 * 1024 * 1024  # 5 MB
    upload_allowed_mime: List[str] = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    ]

    # CORS：与 credentials 共存时不能用 "*"，必须列具体来源
    cors_allow_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_prefix="SERVER_",
        env_file_encoding="utf-8",
    )


settings = Settings()
