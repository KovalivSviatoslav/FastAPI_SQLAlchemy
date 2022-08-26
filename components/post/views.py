from datetime import date
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from components.post import schemas
from components.post.elastic import PostIndexService
from components.post.services import PostService
from components.user.auth import AuthHandler
from components.user.models import User
from config.db import get_session

post_router = APIRouter()


@post_router.get(
    "/posts",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.PostCreateUpdateResponse],
    tags=["posts"]
)
async def list_posts(
        session: AsyncSession = Depends(get_session),
        _: User = Depends(AuthHandler().get_current_user)
):
    posts = await PostService(session).get_posts()
    return posts


@post_router.get(
    "/posts/search",
    status_code=status.HTTP_200_OK,
    tags=["posts"]
)
async def search_posts(
        es_service: PostIndexService = Depends(PostIndexService),
        _: User = Depends(AuthHandler().get_current_user),
        search: Union[str, None] = None,
        category: Union[str, None] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
):
    response = await es_service.search(
        search=search,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    return response


@post_router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostCreateUpdateResponse,
    tags=["posts"]
)
async def create_post(
        payload: schemas.PostCreateUpdateBody,
        session: AsyncSession = Depends(get_session),
        es_service: PostIndexService = Depends(PostIndexService),
        user: User = Depends(AuthHandler().get_current_user)
):
    try:
        post = await PostService(session, es_service).create(
            payload.dict(),
            user.id
        )
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=err.orig.args[0])
    return post


@post_router.get(
    "/posts/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostDetailUpdateResponse,
    tags=["posts"]
)
async def get_post(
        post_id: int,
        session: AsyncSession = Depends(get_session),
        _: User = Depends(AuthHandler().get_current_user)
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
        es_service: PostIndexService = Depends(PostIndexService),
        _: User = Depends(AuthHandler().get_current_user)
):
    await PostService(session, es_service).delete(post_id)
    return {"ok": True}


@post_router.put(
    "/posts/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostCreateUpdateResponse,
    tags=["posts"]
)
async def update_post(
        post_id: int,
        payload: schemas.PostCreateUpdateBody,
        session: AsyncSession = Depends(get_session),
        es_service: PostIndexService = Depends(PostIndexService),
        _: User = Depends(AuthHandler().get_current_user)
):
    try:
        post = await PostService(session, es_service).update(post_id, payload.dict())
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=err.orig.args[0])
    return post
