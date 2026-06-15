"""Comment DAO."""

from typing import List, Optional, Tuple

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.dependencies import get_db_session
from server.models.comment_model import Comment


class CommentDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def list_(
        self,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        approved_only: bool = True,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Comment], int]:
        stmt = select(Comment)
        count_stmt = select(func.count(Comment.id))
        if approved_only:
            stmt = stmt.where(Comment.is_approved.is_(True))
            count_stmt = count_stmt.where(Comment.is_approved.is_(True))
        if target_type:
            stmt = stmt.where(Comment.target_type == target_type)
            count_stmt = count_stmt.where(Comment.target_type == target_type)
        if target_id is not None:
            stmt = stmt.where(Comment.target_id == target_id)
            count_stmt = count_stmt.where(Comment.target_id == target_id)
        stmt = stmt.order_by(Comment.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        total = (await self.session.execute(count_stmt)).scalar_one()
        return list(result.scalars().all()), int(total)

    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        result = await self.session.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Comment:
        obj = Comment(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, comment_id: int, **kwargs) -> Optional[Comment]:
        obj = await self.get_by_id(comment_id)
        if not obj:
            return None
        for k, v in kwargs.items():
            if v is not None:
                setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, comment_id: int) -> bool:
        obj = await self.get_by_id(comment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
