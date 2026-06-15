"""Category DAO."""

from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.dependencies import get_db_session
from server.models.category_model import Category


class CategoryDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def list_all(self) -> List[Category]:
        result = await self.session.execute(
            select(Category).order_by(Category.sort_order.asc(), Category.id.asc()),
        )
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        result = await self.session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.session.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Category:
        obj = Category(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, category_id: int, **kwargs) -> Optional[Category]:
        obj = await self.get_by_id(category_id)
        if not obj:
            return None
        for k, v in kwargs.items():
            if v is not None:
                setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, category_id: int) -> bool:
        obj = await self.get_by_id(category_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
