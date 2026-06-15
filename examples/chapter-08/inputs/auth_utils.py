"""第 8 章自包含示例：与正文 8.2 节四类函数形态一致（无 FastAPI / JWT 依赖，便于 AST 演示）。"""


class BizError(Exception):
    """演示用业务异常（与真实项目 BizError 语义类似）。"""


def hash_password(plain: str) -> str:
    return f"hashed:{plain}"


def verify_password(plain: str, hashed: str) -> bool:
    return hashed == f"hashed:{plain}"


def create_access_token(*, subject: str) -> str:
    return f"jwt-demo:{subject}"


def get_current_user(authorization: str | None = None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise BizError("unauthorized")
    return authorization.removeprefix("Bearer ").strip() or "user"
