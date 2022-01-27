from ..services.auth import AuthService
from ..services.posts import PostService
from ..db.database import database


def get_post_service() -> PostService:
    return PostService(database)


def get_auth_service() -> AuthService:
    return AuthService(database)
