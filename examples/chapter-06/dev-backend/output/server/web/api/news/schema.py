from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class NewsCreate(BaseModel):
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    published_at: Optional[datetime] = None


class NewsUpdate(BaseModel):  # 所有字段可选（PATCH 语义）
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    published_at: Optional[datetime] = None


class NewsResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class NewsListResponse(BaseModel):
    items: List[NewsResponse]
    total: int
