"""User API views for registration and login."""

from fastapi import APIRouter, Depends, HTTPException

from server.dao.user_dao import UserDAO
from server.auth import (
    get_current_user,
    get_current_superuser,
    verify_refresh_token,
)
from server.utils.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from server.models.user_model import User
from server.web.api.response import ApiResponse
from server.web.api.users.schema import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserResponse], status_code=201)
async def register_user(
    user_data: UserCreate,
    user_dao: UserDAO = Depends(),
) -> ApiResponse[UserResponse]:
    """注册新用户。"""
    existing_user = await user_dao.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    existing_email = await user_dao.get_user_by_email(user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    hashed_password = get_password_hash(user_data.password)
    user = await user_dao.create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )
    return ApiResponse.success(data=UserResponse.model_validate(user), msg="注册成功")


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login_user(
    login_data: UserLogin,
    user_dao: UserDAO = Depends(),
) -> ApiResponse[TokenResponse]:
    """用户登录，返回 JWT token。"""
    user = await user_dao.get_user_by_username(login_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="用户已被禁用")

    access_token = create_access_token(data={"user_id": user.id, "username": user.username})
    refresh_token = create_refresh_token(data={"user_id": user.id})

    token_data = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return ApiResponse.success(data=token_data, msg="登录成功")


@router.post("/refresh", response_model=ApiResponse[TokenResponse])
async def refresh_token(
    payload: dict = Depends(verify_refresh_token),
    user_dao: UserDAO = Depends(),
) -> ApiResponse[TokenResponse]:
    """使用 refresh token 刷新 access token。"""
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的 refresh token")

    user = await user_dao.get_user_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="用户不存在或已被禁用")

    access_token = create_access_token(data={"user_id": user.id, "username": user.username})
    refresh_token_new = create_refresh_token(data={"user_id": user.id})

    token_data = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_new,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return ApiResponse.success(data=token_data, msg="刷新成功")


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> ApiResponse[UserResponse]:
    """获取当前登录用户的信息（需要认证）。"""
    return ApiResponse.success(data=UserResponse.model_validate(current_user))
