"""统一响应格式。

- code: 业务状态码 (0=成功, >1000=业务错误)
- msg: 提示信息
- data: 业务数据 (单个对象或列表)
"""

from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

from server.web.api.error_codes import ErrorCode, get_error_message

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式。"""

    code: int = 0
    msg: str = "success"
    data: Optional[T] = None

    @classmethod
    def success(
        cls,
        data: Optional[T] = None,
        msg: str = "success",
    ) -> "ApiResponse[T]":
        """成功响应。"""
        return cls(code=0, msg=msg, data=data)

    @classmethod
    def error(
        cls,
        code: Union[int, ErrorCode] = ErrorCode.BUSINESS_ERROR,
        msg: Optional[str] = None,
    ) -> "ApiResponse[T]":
        """错误响应。"""
        error_code = int(code)
        error_msg = msg or get_error_message(ErrorCode(error_code))
        return cls(code=error_code, msg=error_msg, data=None)


def success_response(data=None, msg: str = "success") -> dict:
    """快捷成功响应函数。"""
    return {"code": 0, "msg": msg, "data": data}


def error_response(
    code: Union[int, ErrorCode] = ErrorCode.BUSINESS_ERROR,
    msg: Optional[str] = None,
) -> dict:
    """快捷错误响应函数。"""
    error_code = int(code)
    error_msg = msg or get_error_message(ErrorCode(error_code))
    return {"code": error_code, "msg": error_msg, "data": None}


def list_response(data: Optional[List] = None, msg: str = "success") -> dict:
    """快捷列表响应函数（空数据返回空数组）。"""
    return {"code": 0, "msg": msg, "data": data if data is not None else []}
