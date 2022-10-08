from datetime import datetime
from typing import List, Optional
from uuid import UUID

from domain.posts.repositories import posts
from shared import container
from shared.applications import BaseAppModel


class PostListModel(BaseAppModel):
    id: UUID
    user_id: UUID
    title: str
    content: Optional[str]
    is_published: Optional[bool]
    photo: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes: Optional[List[int]]


class PostsListOutput(BaseAppModel):
    posts: List[PostListModel]


@container.register
class GetPostsList(object):
    def __int__(self, posts_repository: posts.PostAppRepository):
        self._posts = posts_repository

    async def __call__(self) -> PostsListOutput:
        posts_list = await self._posts.get_all_posts()
        response_list = [PostListModel(**post.dict()) for post in posts_list]

        return PostsListOutput(posts=response_list)
