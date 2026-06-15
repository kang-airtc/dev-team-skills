"""News schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NewsBase(BaseModel):
    title: str
    slug: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    content: str
    author: Optional[str] = None
    is_published: bool = True
    published_at: Optional[datetime] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    is_published: Optional[bool] = None
    published_at: Optional[datetime] = None


class NewsResponse(NewsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class NewsListResponse(BaseModel):
    items: list[NewsResponse]
    total: int
