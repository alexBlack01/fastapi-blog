from .users import users
from .posts import posts
from .database import metadata, engine

metadata.create_all(bind=engine)
