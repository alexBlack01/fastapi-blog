from typing import List

from fastapi import (
    HTTPException,
    status,
    UploadFile
)

from ..db import posts
from databases import Database
from ..models.posts import (
    PostCreate,
    PostUpdate,
    Post,
    PostList,
    PostWithDetails
)


class PostService:
    def __init__(self, database: Database):
        self.database = database

    async def _get(self, post_id: int) -> PostWithDetails:
        query = posts.select().where(posts.c.id == post_id)
        post = await self.database.fetch_one(query=query)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return PostWithDetails.parse_obj(post)

    async def get_list(self, limit: int = 100, skip: int = 0) -> List[PostList]:
        query = posts.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get(self, post_id: int) -> PostWithDetails:
        return await self._get(post_id)

    async def create(self, user_id: int,
                     post_data: PostCreate, file_data: UploadFile) -> Post:

        file_name = file_data.filename
        with open(f'media/{file_name}', 'w') as file:
            file.close()

        post = Post(
            **post_data.dict(),
            user_id=user_id,
            photo=file_name
        )

        values = {**post.dict()}
        query = posts.insert().values(**values)
        await self.database.execute(query=query)

        return post

    async def update(self, user_id: int, post_id: int,
                     post_data: PostUpdate, file_data: UploadFile) -> Post:
        post = await self._get(post_id)

        if post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        file_name = file_data.filename
        with open(f'media/{file_name}', 'w') as file:
            file.close()

        for field, value in post_data:
            if value:
                setattr(post, field, value)

        post.photo = file_name

        values = {**post.dict()}
        query = posts.update().where(posts.c.id == post_id).values(**values)
        await self.database.execute(query=query)
        return post

    async def delete(self, user_id: int, post_id: int):
        post = await self._get(post_id)

        if post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        query = posts.delete().where(posts.c.id == post_id)
        return await self.database.execute(query=query)

    async def set_like(self, user_id: int, post_id: int) -> Post:
        post = await self._get(post_id)

        values = {**post.dict()}
        likes_data = values.get("likes")

        if likes_data is None:
            likes_data = [user_id]
        elif user_id in likes_data:
            likes_data.remove(user_id)
        else:
            likes_data.append(user_id)

        values.update(likes=likes_data)

        query = posts.update().where(posts.c.id == post_id).values(**values)
        await self.database.execute(query=query)

        post = await self._get(post_id)
        return post
