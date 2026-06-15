"""News API views."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from server.auth import get_current_user
from server.dao.news_dao import NewsDAO
from server.models.user_model import User
from server.web.api.news.schema import (
    NewsCreate,
    NewsListResponse,
    NewsResponse,
    NewsUpdate,
)
from server.web.api.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[NewsListResponse])
async def list_news(
    include_unpublished: bool = Query(False),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    dao: NewsDAO = Depends(),
) -> ApiResponse[NewsListResponse]:
    items, total = await dao.list_(
        published_only=not include_unpublished,
        limit=limit,
        offset=offset,
    )
    return ApiResponse.success(
        data=NewsListResponse(
            items=[NewsResponse.model_validate(i) for i in items],
            total=total,
        ),
    )


@router.get("/slug/{slug}", response_model=ApiResponse[NewsResponse])
async def get_news_by_slug(slug: str, dao: NewsDAO = Depends()) -> ApiResponse[NewsResponse]:
    obj = await dao.get_by_slug(slug)
    if not obj or not obj.is_published:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=NewsResponse.model_validate(obj))


@router.get("/{news_id}", response_model=ApiResponse[NewsResponse])
async def get_news(news_id: int, dao: NewsDAO = Depends()) -> ApiResponse[NewsResponse]:
    obj = await dao.get_by_id(news_id)
    if not obj:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=NewsResponse.model_validate(obj))


@router.post("", response_model=ApiResponse[NewsResponse], status_code=201)
async def create_news(
    payload: NewsCreate,
    dao: NewsDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[NewsResponse]:
    if await dao.get_by_slug(payload.slug):
        raise HTTPException(status_code=400, detail="slug 已存在")
    data = payload.model_dump()
    if data.get("is_published") and not data.get("published_at"):
        data["published_at"] = datetime.now(timezone.utc)
    obj = await dao.create(**data)
    return ApiResponse.success(data=NewsResponse.model_validate(obj), msg="创建成功")


@router.put("/{news_id}", response_model=ApiResponse[NewsResponse])
async def update_news(
    news_id: int,
    payload: NewsUpdate,
    dao: NewsDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[NewsResponse]:
    obj = await dao.update(news_id, **payload.model_dump(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data=NewsResponse.model_validate(obj), msg="更新成功")


@router.delete("/{news_id}", response_model=ApiResponse[dict])
async def delete_news(
    news_id: int,
    dao: NewsDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[dict]:
    ok = await dao.delete(news_id)
    if not ok:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return ApiResponse.success(data={"id": news_id}, msg="删除成功")
