"""Comment API views.

公开端：
- GET  /comments?target_type=&target_id=  列出已审核评论
- POST /comments                          匿名/登录用户均可发表（默认直接审核通过）

后台：
- GET    /comments/admin    所有评论（含未审核）
- PUT    /comments/{id}     审核 / 反审核
- DELETE /comments/{id}     删除
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from server.auth import get_current_user
from server.dao.comment_dao import CommentDAO
from server.models.user_model import User
from server.web.api.comments.schema import (
    CommentCreate,
    CommentListResponse,
    CommentResponse,
    CommentUpdate,
)
from server.web.api.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[CommentListResponse])
async def list_comments(
    target_type: Optional[str] = Query(None, pattern="^(product|news)$"),
    target_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    dao: CommentDAO = Depends(),
) -> ApiResponse[CommentListResponse]:
    items, total = await dao.list_(
        target_type=target_type,
        target_id=target_id,
        approved_only=True,
        limit=limit,
        offset=offset,
    )
    return ApiResponse.success(
        data=CommentListResponse(
            items=[CommentResponse.model_validate(i) for i in items],
            total=total,
        ),
    )


@router.post("", response_model=ApiResponse[CommentResponse], status_code=201)
async def create_comment(
    payload: CommentCreate,
    dao: CommentDAO = Depends(),
) -> ApiResponse[CommentResponse]:
    data = payload.model_dump()
    data["is_approved"] = True
    obj = await dao.create(**data)
    return ApiResponse.success(data=CommentResponse.model_validate(obj), msg="评论成功")


@router.get("/admin", response_model=ApiResponse[CommentListResponse])
async def list_comments_admin(
    target_type: Optional[str] = Query(None, pattern="^(product|news)$"),
    target_id: Optional[int] = Query(None),
    approved_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    dao: CommentDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[CommentListResponse]:
    items, total = await dao.list_(
        target_type=target_type,
        target_id=target_id,
        approved_only=approved_only,
        limit=limit,
        offset=offset,
    )
    return ApiResponse.success(
        data=CommentListResponse(
            items=[CommentResponse.model_validate(i) for i in items],
            total=total,
        ),
    )


@router.put("/{comment_id}", response_model=ApiResponse[CommentResponse])
async def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    dao: CommentDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[CommentResponse]:
    obj = await dao.update(comment_id, **payload.model_dump(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="评论不存在")
    return ApiResponse.success(data=CommentResponse.model_validate(obj), msg="更新成功")


@router.delete("/{comment_id}", response_model=ApiResponse[dict])
async def delete_comment(
    comment_id: int,
    dao: CommentDAO = Depends(),
    _: User = Depends(get_current_user),
) -> ApiResponse[dict]:
    ok = await dao.delete(comment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="评论不存在")
    return ApiResponse.success(data={"id": comment_id}, msg="删除成功")
