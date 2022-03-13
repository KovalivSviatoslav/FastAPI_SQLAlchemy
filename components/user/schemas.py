from pydantic import BaseModel

from components.user.models import BaseUser


class UserCreateSchema(BaseUser):
    password: str


class SignInSchema(BaseModel):
    email: str
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str


class UserDetailSchema(BaseModel):
    firstname: str
    lastname: str
