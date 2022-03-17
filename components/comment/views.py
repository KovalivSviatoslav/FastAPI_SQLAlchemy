from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from components.comment import schemas
from components.comment.services import CommentService
from components.user.auth import AuthHandler
from components.user.models import User
from config.db import get_session

comment_router = APIRouter()


@comment_router.post(
    "/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CommentDetailResponse,
    tags=["comments"]
)
async def create_comment(
        payload: schemas.CommentCreateBody,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(AuthHandler().get_current_user)
):
    comment = await CommentService(session).create(payload.dict(), user.id)
    return comment


@comment_router.put(
    "/comments/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.CommentDetailResponse,
    tags=["posts"]
)
async def update_post(
    comment_id: int,
    payload: schemas.CommentUpdateBody,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(AuthHandler().get_current_user)
):
    try:
        post = await CommentService(session).update(comment_id, payload.dict())
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=err.orig.args[0])
    return post


@comment_router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["posts"]
)
async def delete_post(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(AuthHandler().get_current_user)
):
    await CommentService(session).delete(comment_id)
    return {"ok": True}
