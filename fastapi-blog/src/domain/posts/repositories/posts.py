import abc
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from shared.applications import BaseAppModel


class Post(BaseAppModel):
    id: UUID
    user_id: UUID
    title: str
    content: Optional[str]
    is_published: Optional[bool]
    photo: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes: Optional[List[int]]


class PostAppRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all_posts(self) -> List[Post]:
        raise NotImplementedError
