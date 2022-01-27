import sqlalchemy as sa
from .database import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("email", sa.String, unique=True),
    sa.Column("username", sa.String, unique=True),
    sa.Column("password_hash", sa.Text)
)
