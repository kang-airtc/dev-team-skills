"""文件上传接口。

- POST /api/uploads —— 单文件上传（multipart/form-data, 字段名 file）
- 仅允许图片，最大 5MB
- 文件保存到 settings.upload_dir 下，按 YYYY/MM 子目录归档
- 返回相对 URL（如 /uploads/2026/04/xxxxx.jpg），由前端拼上 host
"""

from __future__ import annotations

import secrets
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from server.auth import get_current_user
from server.models.user_model import User
from server.settings import settings
from server.web.api.response import ApiResponse

router = APIRouter()


# 后缀映射（防止用户上传的扩展名被信任）
_MIME_TO_EXT = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


def _save_image(file: UploadFile, content: bytes) -> str:
    if file.content_type not in settings.upload_allowed_mime:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型：{file.content_type}",
        )
    if len(content) > settings.upload_max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，最大允许 {settings.upload_max_bytes // 1024 // 1024} MB",
        )

    ext = _MIME_TO_EXT.get(file.content_type, ".bin")
    now = datetime.now()
    sub_dir = Path(f"{now.year:04d}") / f"{now.month:02d}"
    target_dir: Path = settings.upload_dir / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    name = f"{secrets.token_hex(12)}{ext}"
    target_path = target_dir / name
    target_path.write_bytes(content)

    rel_url = f"{settings.upload_url_prefix}/{sub_dir.as_posix()}/{name}"
    return rel_url


@router.post("", response_model=ApiResponse[dict])
async def upload_file(
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
) -> ApiResponse[dict]:
    """单文件上传，返回 {url, size, mime}。"""
    content = await file.read()
    url = _save_image(file, content)
    return ApiResponse.success(
        data={"url": url, "size": len(content), "mime": file.content_type},
    )


@router.post("/multi", response_model=ApiResponse[dict])
async def upload_files(
    files: List[UploadFile] = File(...),
    _: User = Depends(get_current_user),
) -> ApiResponse[dict]:
    """多文件上传，返回 {urls: [...]}。"""
    urls = []
    for f in files:
        content = await f.read()
        urls.append(_save_image(f, content))
    return ApiResponse.success(data={"urls": urls})
