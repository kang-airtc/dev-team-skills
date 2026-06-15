"""Category API views."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from server.auth import get_current_user
from server.dao.category_dao import CategoryDAO
from server.models.user_model import User
from server.web.api.categories.schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from server.web.api.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[List[CategoryResponse]])
async def list_categories(dao: CategoryDAO = Depends()) -> ApiResponse[List[CategoryResponse]]:
    items = await dao.list_all()
    return ApiResponse.success(data=[CategoryResponse.model_validate(i) for i in items])


@router.post("", response_model=ApiResponse[CategoryResponse], status_code=201)
async def create_category(
    payload: CategoryCreate,
    dao: CategoryDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[CategoryResponse]:
    if await dao.get_by_slug(payload.slug):
        raise HTTPException(status_code=400, detail="slug 已存在")
    obj = await dao.create(**payload.model_dump())
    return ApiResponse.success(data=CategoryResponse.model_validate(obj), msg="创建成功")


@router.put("/{category_id}", response_model=ApiResponse[CategoryResponse])
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    dao: CategoryDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[CategoryResponse]:
    obj = await dao.update(category_id, **payload.model_dump(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="分类不存在")
    return ApiResponse.success(data=CategoryResponse.model_validate(obj), msg="更新成功")


@router.delete("/{category_id}", response_model=ApiResponse[dict])
async def delete_category(
    category_id: int,
    dao: CategoryDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[dict]:
    ok = await dao.delete(category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="分类不存在")
    return ApiResponse.success(data={"id": category_id}, msg="删除成功")
