import sqlalchemy as sa
from .database import metadata

posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id')),
    sa.Column("title", sa.String, nullable=False),
    sa.Column("content", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()),
    sa.Column("photo", sa.String),
    sa.Column("is_published", sa.Boolean, default=False),
    sa.Column("likes", sa.ARRAY(sa.Integer), nullable=True)
)



