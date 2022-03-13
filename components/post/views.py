from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from components.post import schemas
from components.post.services import PostService
from components.user.auth import AuthHandler
from components.user.models import User
from config.db import get_session

post_router = APIRouter()


@post_router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostCreateResponse,
    # response_model_exclude={"comments"},
    tags=["posts"]
)
async def create_post(
        payload: schemas.PostCreateBody,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(AuthHandler().get_current_user)
):
    try:
        post = await PostService(session).create(payload.dict(), user.id)
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=err.orig.args[0])
    return post


@post_router.get(
    "/posts/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostDetailResponse,
    tags=["posts"]
)
async def get_post(
        post_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(AuthHandler().get_current_user)
):
    post = await PostService(session).get_post_by_id(post_id=post_id)
    return post


@post_router.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["posts"]
)
async def delete_post(
        post_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(AuthHandler().get_current_user)
):
    await PostService(session).delete(post_id)
    return {"ok": True}
