from datetime import datetime
from typing import Optional, List

from fastapi import Form
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: Optional[str]
    is_published: Optional[bool]
    photo: str


class PostList(BaseModel):
    pass


class Post(PostBase):
    user_id: int
    likes: Optional[List[int]]


class PostWithDetails(Post):
    created_at: datetime
    updated_at: datetime


class PostCreate(BaseModel):
    title: str
    content: Optional[str]
    is_published: Optional[bool]

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
            content: Optional[str] = Form(None),
            is_published: Optional[bool] = Form(None)):
        return cls(title=title, content=content, is_published=is_published)


class PostUpdate(PostCreate):
    pass
