"""Product API views."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from server.auth import get_current_user
from server.dao.product_dao import ProductDAO
from server.models.user_model import User
from server.web.api.products.schema import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from server.web.api.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[ProductListResponse])
async def list_products(
    category_id: Optional[int] = Query(None),
    is_featured: Optional[bool] = Query(None),
    include_unpublished: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    dao: ProductDAO = Depends(),
) -> ApiResponse[ProductListResponse]:
    items, total = await dao.list_(
        category_id=category_id,
        is_featured=is_featured,
        published_only=not include_unpublished,
        limit=limit,
        offset=offset,
    )
    return ApiResponse.success(
        data=ProductListResponse(
            items=[ProductResponse.model_validate(i) for i in items],
            total=total,
        ),
    )


@router.get("/slug/{slug}", response_model=ApiResponse[ProductResponse])
async def get_product_by_slug(slug: str, dao: ProductDAO = Depends()) -> ApiResponse[ProductResponse]:
    obj = await dao.get_by_slug(slug)
    if not obj or not obj.is_published:
        raise HTTPException(status_code=404, detail="产品不存在")
    return ApiResponse.success(data=ProductResponse.model_validate(obj))


@router.get("/{product_id}", response_model=ApiResponse[ProductResponse])
async def get_product(
    product_id: int,
    dao: ProductDAO = Depends(),
) -> ApiResponse[ProductResponse]:
    obj = await dao.get_by_id(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="产品不存在")
    return ApiResponse.success(data=ProductResponse.model_validate(obj))


@router.post("", response_model=ApiResponse[ProductResponse], status_code=201)
async def create_product(
    payload: ProductCreate,
    dao: ProductDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[ProductResponse]:
    if await dao.get_by_slug(payload.slug):
        raise HTTPException(status_code=400, detail="slug 已存在")
    obj = await dao.create(**payload.model_dump())
    return ApiResponse.success(data=ProductResponse.model_validate(obj), msg="创建成功")


@router.put("/{product_id}", response_model=ApiResponse[ProductResponse])
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    dao: ProductDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[ProductResponse]:
    obj = await dao.update(product_id, **payload.model_dump(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="产品不存在")
    return ApiResponse.success(data=ProductResponse.model_validate(obj), msg="更新成功")


@router.delete("/{product_id}", response_model=ApiResponse[dict])
async def delete_product(
    product_id: int,
    dao: ProductDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[dict]:
    ok = await dao.delete(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="产品不存在")
    return ApiResponse.success(data={"id": product_id}, msg="删除成功")
