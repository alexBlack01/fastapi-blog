from fastapi import APIRouter

from domain.posts.usecases import get_posts_list
from shared import container, exceptions

router = APIRouter()


@router.get(
    '/',
    summary='Get all posts list',
    response_model=get_posts_list.PostsListOutput,
    responses=exceptions.exception_schema([]),
)
async def get_list():
    case = container.resolve(get_posts_list.GetPostsList)
    return await case()
