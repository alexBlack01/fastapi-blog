from fastapi import APIRouter

from applications.rest.v1 import posts

router = APIRouter()
router.include_router(posts.router, prefix='/posts', tags=['posts'])
