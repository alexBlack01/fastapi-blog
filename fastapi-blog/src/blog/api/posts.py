from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    UploadFile,
    File
)

from .depends import get_post_service
from ..models.posts import (
    Post,
    PostCreate,
    PostUpdate,
    PostList,
    PostWithDetails
)
from ..models.users import User
from ..services.auth import get_current_user
from ..services.posts import PostService

router = APIRouter(
    prefix='/posts',
)


@router.get("/", response_model=List[PostList])
async def get_posts(
        limit: int = 100,
        skip: int = 0,
        service: PostService = Depends(get_post_service)
):
    return await service.get_list(limit, skip)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
        post_data: PostCreate = Depends(PostCreate.as_form),
        user: User = Depends(get_current_user),
        service: PostService = Depends(get_post_service),
        file_data: UploadFile = File(...)
):
    return await service.create(user.id, post_data, file_data)


@router.post("/{post_id}/like", response_model=Post, status_code=status.HTTP_200_OK)
async def set_like(
    post_id: int,
    user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    return await service.set_like(user.id, post_id)


@router.get("/{post_id}", response_model=PostWithDetails)
async def get_post(
    post_id: int,
    service: PostService = Depends(get_post_service)
):
    return await service.get(post_id)


@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_data: PostUpdate = Depends(PostUpdate.as_form),
    user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
    file_data: UploadFile = File(...)
):
    return await service.update(user.id, post_id, post_data, file_data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    await service.delete(user.id, post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
