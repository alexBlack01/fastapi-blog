from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    password_hash: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
