"""Comment API views."""
from fastapi import APIRouter, Depends, HTTPException

from server.dao.comment_dao import CommentDAO
from server.web.api.comments.schema import CommentCreate, CommentResponse

router = APIRouter()


@router.get("/{news_id}/comments")
async def get_comments(news_id: int, dao: CommentDAO = Depends()):
    items = await dao.list_by_news(news_id)
    return {"code": 0, "data": items}


@router.post("/{news_id}/comments")
async def add_comment(
    news_id: int,
    payload: CommentCreate,
    dao: CommentDAO = Depends(),
):
    if not payload.content or len(payload.content.strip()) == 0:
        raise HTTPException(status_code=400, detail="评论内容不能为空")

    obj = await dao.create(news_id=news_id, **payload.model_dump())
    return {"code": 0, "msg": "ok", "data": {"id": obj.id}}


@router.delete("/{news_id}/comments/{comment_id}")
async def deleteComment(
    news_id: int,
    comment_id: int,
    dao: CommentDAO = Depends(),
):
    result = await dao.delete(comment_id)
    if not result:
        raise HTTPException(status_code=404, detail="评论不存在")
    print(f"评论 {comment_id} 已删除")
    return {"code": 0, "msg": "删除成功", "data": None}


@router.get("/{news_id}/comments/count")
async def get_comment_count(news_id: int, dao: CommentDAO = Depends()):
    items = await dao.list_by_news(news_id)
    return {"code": 0, "data": {"count": len(items)}}
