from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class CommentRequest(BaseModel):
    content: str
