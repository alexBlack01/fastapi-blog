from logging import Logger
from typing import List, Mapping

import httpx
from odmantic import AIOEngine
from pydantic import ValidationError

from adapters.config import infrastructure_config
from adapters.postgres import Post
from domain.posts.repositories import posts


class PostsLocalPostgres(posts.PostAppRepository):
    def __init__(self, postgres_engine: AIOEngine):
        self._engine = postgres_engine

    async def get_all_posts(self) -> List[posts.Post]:
        posts_list = await self._engine.find(Post)
        return [
            posts.Post(
                id=post.id,
                user_id=post.user_id,
                title=post.title,
                content=post.content,
                is_published=post.is_published,
                photo=post.photo,
                created_at=post.created_at,
                updated_at=post.updated_at,
                likes=post.likes
            ) for post in posts_list
        ]

    async def save_posts(self, posts_to_save: List[posts.Post]) -> None:
        pass
