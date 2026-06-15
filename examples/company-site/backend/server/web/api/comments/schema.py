"""Comment schemas."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CommentCreate(BaseModel):
    target_type: Literal["product", "news"]
    target_id: int
    nickname: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)

    @field_validator("nickname", "content")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class CommentUpdate(BaseModel):
    is_approved: Optional[bool] = None


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    target_type: str
    target_id: int
    user_id: Optional[int]
    nickname: str
    content: str
    is_approved: bool
    created_at: datetime


class CommentListResponse(BaseModel):
    items: list[CommentResponse]
    total: int
