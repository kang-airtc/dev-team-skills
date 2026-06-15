from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from server.dao.news_dao import NewsDAO
from server.models.user_model import User
from server.utils.auth import get_current_user
from server.utils.response import ApiResponse
from .schema import NewsCreate, NewsListResponse, NewsResponse, NewsUpdate


router = APIRouter()

@router.get("", response_model=ApiResponse[NewsListResponse])
async def list_news(
    limit: int = 10,
    offset: int = 0,
    dao: NewsDAO = Depends(),
) -> ApiResponse[NewsListResponse]:
    items, total = await dao.list_(limit=limit, offset=offset)
    data = NewsListResponse(
        items=[NewsResponse.model_validate(i) for i in items],
        total=total,
    )
    return ApiResponse.success(data=data)

@router.get("/slug/{slug}", response_model=ApiResponse[NewsResponse])
async def get_news_by_slug(
    slug: str,
    dao: NewsDAO = Depends(),
) -> ApiResponse[NewsResponse]:
    obj = await dao.get_by_slug(slug=slug)
    if not obj:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=NewsResponse.model_validate(obj))

@router.get("/{news_id}", response_model=ApiResponse[NewsResponse])
async def get_news(
    news_id: int,
    dao: NewsDAO = Depends(),
) -> ApiResponse[NewsResponse]:
    obj = await dao.get_by_id(news_id=news_id)
    if not obj:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=NewsResponse.model_validate(obj))

@router.post("", response_model=ApiResponse[NewsResponse])
async def create_news(
    body: NewsCreate,
    dao: NewsDAO = Depends(),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[NewsResponse]:
    obj = await dao.create(**body.model_dump())
    return ApiResponse.success(data=NewsResponse.model_validate(obj))

@router.put("/{news_id}", response_model=ApiResponse[NewsResponse])
async def update_news(
    news_id: int,
    body: NewsUpdate,
    dao: NewsDAO = Depends(),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[NewsResponse]:
    obj = await dao.update(news_id=news_id, data=body.model_dump(exclude_none=True))
    if not obj:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=NewsResponse.model_validate(obj))

@router.delete("/{news_id}", response_model=ApiResponse[None])
async def delete_news(
    news_id: int,
    dao: NewsDAO = Depends(),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[None]:
    ok = await dao.delete(news_id=news_id)
    if not ok:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=None)
