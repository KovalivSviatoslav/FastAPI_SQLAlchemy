from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from components.user.auth import AuthHandler
from components.user.schemas import UserCreateSchema, AccessTokenSchema, SignInSchema
from components.user.services import UserService
from config.db import get_session

user_router = APIRouter()


@user_router.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AccessTokenSchema,
    tags=["users"]
)
async def register(payload: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).get_user_by_email(payload.email)
    if user:
        raise HTTPException(detail="Email already registered.", status_code=status.HTTP_409_CONFLICT)

    payload.password = AuthHandler().get_password_hash(payload.password)
    user = await UserService(session).create(data=payload.dict())
    access_token = AuthHandler().encode_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post(
    "/users/login",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenSchema,
    tags=["users"]
)
async def login(payload: SignInSchema, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).get_user_by_email(payload.email)
    if not user:
        raise HTTPException(
            detail=f"User with email {payload.email} does not exists.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    if not AuthHandler().verify_password(payload.password, user.password):
        raise HTTPException(
            detail=f"Incorrect password.",
            status_code=status.HTTP_403_FORBIDDEN
        )

    access_token = AuthHandler().encode_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
