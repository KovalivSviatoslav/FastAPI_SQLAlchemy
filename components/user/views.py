from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from components.user.schemas import UserCreateSchema, UserResponseSchema
from components.user.services import UserService
from config.db import get_session

user_router = APIRouter()


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema, tags=["users"])
async def register(payload: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).create(data=payload.dict())
    return user
