from __future__ import annotations

from typing import List, Optional, Tuple

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.news_model import News
from server.utils.db import get_db_session


class NewsDAO:
    """Data Access Object for News."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def list_(
        self,
        limit: int = 10,
        offset: int = 0,
        published_only: bool = True,
    ) -> Tuple[List[News], int]:
        stmt = select(News)
        if published_only:
            stmt = stmt.where(News.is_published.is_(True))
        stmt = stmt.order_by(News.published_at.desc())

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total: int = (await self.session.execute(count_stmt)).scalar_one()

        rows = (await self.session.execute(stmt.limit(limit).offset(offset))).scalars().all()
        return list(rows), total

    async def get_by_id(self, news_id: int) -> Optional[News]:
        stmt = select(News).where(News.id == news_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[News]:
        stmt = select(News).where(News.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **data) -> News:
        obj = News(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, news_id: int, data: dict) -> Optional[News]:
        obj = await self.get_by_id(news_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, news_id: int) -> bool:
        obj = await self.get_by_id(news_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
