"""Product DAO."""

from typing import List, Optional, Tuple

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.dependencies import get_db_session
from server.models.product_model import Product


class ProductDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def list_(
        self,
        category_id: Optional[int] = None,
        is_featured: Optional[bool] = None,
        published_only: bool = True,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Product], int]:
        stmt = select(Product)
        count_stmt = select(func.count(Product.id))
        if published_only:
            stmt = stmt.where(Product.is_published.is_(True))
            count_stmt = count_stmt.where(Product.is_published.is_(True))
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
            count_stmt = count_stmt.where(Product.category_id == category_id)
        if is_featured is not None:
            stmt = stmt.where(Product.is_featured.is_(is_featured))
            count_stmt = count_stmt.where(Product.is_featured.is_(is_featured))
        stmt = stmt.order_by(Product.sort_order.asc(), Product.id.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        total = (await self.session.execute(count_stmt)).scalar_one()
        return list(result.scalars().all()), int(total)

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        result = await self.session.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Product:
        obj = Product(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, product_id: int, **kwargs) -> Optional[Product]:
        obj = await self.get_by_id(product_id)
        if not obj:
            return None
        for k, v in kwargs.items():
            if v is not None:
                setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, product_id: int) -> bool:
        obj = await self.get_by_id(product_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
