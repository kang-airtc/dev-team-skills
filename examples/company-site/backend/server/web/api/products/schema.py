"""Product schemas."""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    slug: str
    category_id: Optional[int] = None
    tagline: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    gallery: Optional[str] = None
    specs: Optional[str] = None
    price: Optional[Decimal] = None
    is_featured: bool = False
    is_published: bool = True
    sort_order: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    tagline: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    gallery: Optional[str] = None
    specs: Optional[str] = None
    price: Optional[Decimal] = None
    is_featured: Optional[bool] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
