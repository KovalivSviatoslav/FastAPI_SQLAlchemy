from components.user.models import BaseUser


class UserCreateSchema(BaseUser):
    password: str


class UserResponseSchema(BaseUser):
    id: int
