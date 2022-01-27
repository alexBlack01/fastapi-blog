from datetime import (
    datetime,
    timedelta,
)
from fastapi import (
    HTTPException,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError

from databases import Database

from ..db.users import users
from ..models.users import (
    User,
    Token,
    UserCreate
)
from ..config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        return Token(access_token=token)

    def __init__(self, database: Database):
        self.database = database

    async def register_new_user(self, user_data: UserCreate) -> Token:

        user = User(
            id=0,
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )

        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        await self.database.execute(query=query)

        query = users.select().where(users.c.username == user_data.username)
        user = await self.database.fetch_one(query)

        return self.create_token(User.parse_obj(user))

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        query = users.select().where(users.c.username == username)
        user = await self.database.fetch_one(query)

        if not user:
            raise exception

        user = User.parse_obj(user)

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
