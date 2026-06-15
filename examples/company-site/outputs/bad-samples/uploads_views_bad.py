"""教学素材：故意埋 bug 的上传接口对照版本（不可运行）。

第 12 章用它给 dev-backend-lint / review-code 提供真实反面教材。
**不要**把这个文件挂到正式路由——只用于演示 Skill 的扫描效果。

故意埋下的违规：
- B1：缺少文件大小校验（任意大小都能穿透）
- B2：文件句柄未关闭（直接 open / write，未走上下文管理器）
- B3：MIME 类型仅信任前端传值，没有白名单校验
- B4：异常处理使用裸 except，吞掉了所有错误
- B5：返回结构未走统一 ApiResponse 格式
"""

from __future__ import annotations

import secrets
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from server.auth import get_current_user
from server.models.user_model import User
from server.settings import settings

router = APIRouter()


def save_image_bad(file: UploadFile, content: bytes) -> str:
    ext = "." + file.content_type.split("/")[-1]
    now = datetime.now()
    sub_dir = Path(f"{now.year:04d}") / f"{now.month:02d}"
    target_dir: Path = settings.upload_dir / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    name = f"{secrets.token_hex(12)}{ext}"
    target_path = target_dir / name

    f = open(target_path, "wb")
    f.write(content)

    rel_url = f"{settings.upload_url_prefix}/{sub_dir.as_posix()}/{name}"
    return rel_url


@router.post("")
async def upload_file_bad(
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
):
    try:
        content = await file.read()
        url = save_image_bad(file, content)
        return {"url": url, "size": len(content), "mime": file.content_type}
    except:
        return {"error": "upload failed"}
