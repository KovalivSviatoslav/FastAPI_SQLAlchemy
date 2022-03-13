from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from components.comment.schemas import CommentDetailSchema, CommentCreateSchema
from components.comment.services import CommentService
from components.user.auth import AuthHandler
from components.user.models import User
from config.db import get_session

comment_router = APIRouter()


@comment_router.post(
    "/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentDetailSchema,
    tags=["comments"]
)
async def create_comment(
        payload: CommentCreateSchema,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(AuthHandler().get_current_user)
):
    comment = await CommentService(session).create(payload.dict(), user.id)
    return comment
