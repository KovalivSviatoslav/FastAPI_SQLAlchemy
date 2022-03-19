from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from components.rating import schemas
from components.rating.services import RatingService
from components.user.auth import AuthHandler
from components.user.models import User
from config.db import get_session

rating_router = APIRouter()


@rating_router.post(
    "/ratings",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RatingDetailResponse,
    tags=["comments"]
)
async def create_rating(
        payload: schemas.RatingCreateBody,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(AuthHandler().get_current_user)
):
    rating = await RatingService(session).create(payload.dict(), user.id)
    return rating


@rating_router.put(
    "/ratings/{rating_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.RatingDetailResponse,
    tags=["posts"]
)
async def update_rating(
    rating_id: int,
    payload: schemas.RatingUpdateBody,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(AuthHandler().get_current_user)
):
    try:
        rating = await RatingService(session).update(rating_id, payload.dict())
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=err.orig.args[0])
    return rating
