"""News DAO."""

from typing import List, Optional, Tuple

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.dependencies import get_db_session
from server.models.news_model import News


class NewsDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def list_(
        self,
        published_only: bool = True,
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[News], int]:
        stmt = select(News)
        count_stmt = select(func.count(News.id))
        if published_only:
            stmt = stmt.where(News.is_published.is_(True))
            count_stmt = count_stmt.where(News.is_published.is_(True))
        stmt = stmt.order_by(News.published_at.desc().nulls_last(), News.id.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        total = (await self.session.execute(count_stmt)).scalar_one()
        return list(result.scalars().all()), int(total)

    async def get_by_id(self, news_id: int) -> Optional[News]:
        result = await self.session.execute(select(News).where(News.id == news_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[News]:
        result = await self.session.execute(select(News).where(News.slug == slug))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> News:
        obj = News(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, news_id: int, **kwargs) -> Optional[News]:
        obj = await self.get_by_id(news_id)
        if not obj:
            return None
        for k, v in kwargs.items():
            if v is not None:
                setattr(obj, k, v)
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
