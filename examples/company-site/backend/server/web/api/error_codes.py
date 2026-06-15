"""Business error code definitions.

Error code specification:
- 0: Success
- 1000-1999: General errors (param, auth, permission, rate-limit, database)
- 2000-2999: Business errors (user / content / message modules)
"""

from enum import IntEnum


class ErrorCode(IntEnum):
    """Business error code enumeration."""

    # Success
    SUCCESS = 0

    # General errors (1000-1099)
    PARAM_ERROR = 1000
    BUSINESS_ERROR = 1001
    DATA_ERROR = 1002
    PERMISSION_DENIED = 1003
    RESOURCE_NOT_FOUND = 1004
    OPERATION_FAILED = 1005

    # Auth errors (1100-1199)
    USER_NOT_FOUND = 1100
    USER_ALREADY_EXISTS = 1101
    USER_DISABLED = 1102
    INVALID_CREDENTIALS = 1103
    TOKEN_EXPIRED = 1104
    TOKEN_INVALID = 1105

    # Database errors (1300-1399)
    DATABASE_ERROR = 1300
    DATABASE_CONNECTION_ERROR = 1301
    DUPLICATE_ENTRY = 1302

    # Content errors (2000-2099)
    PRODUCT_NOT_FOUND = 2000
    NEWS_NOT_FOUND = 2001
    MESSAGE_SEND_FAILED = 2002


ERROR_MESSAGES = {
    ErrorCode.SUCCESS: "success",
    ErrorCode.PARAM_ERROR: "Parameter error",
    ErrorCode.BUSINESS_ERROR: "Business logic error",
    ErrorCode.DATA_ERROR: "Data processing error",
    ErrorCode.PERMISSION_DENIED: "Permission denied",
    ErrorCode.RESOURCE_NOT_FOUND: "Resource not found",
    ErrorCode.OPERATION_FAILED: "Operation failed",
    ErrorCode.USER_NOT_FOUND: "User not found",
    ErrorCode.USER_ALREADY_EXISTS: "User already exists",
    ErrorCode.USER_DISABLED: "User disabled",
    ErrorCode.INVALID_CREDENTIALS: "Invalid username or password",
    ErrorCode.TOKEN_EXPIRED: "Token expired",
    ErrorCode.TOKEN_INVALID: "Token invalid",
    ErrorCode.DATABASE_ERROR: "Database error",
    ErrorCode.DATABASE_CONNECTION_ERROR: "Database connection error",
    ErrorCode.DUPLICATE_ENTRY: "Duplicate entry",
    ErrorCode.PRODUCT_NOT_FOUND: "Product not found",
    ErrorCode.NEWS_NOT_FOUND: "News article not found",
    ErrorCode.MESSAGE_SEND_FAILED: "Message send failed",
}


def get_error_message(code: ErrorCode) -> str:
    """Get default message for error code."""
    return ERROR_MESSAGES.get(code, "Unknown error")
