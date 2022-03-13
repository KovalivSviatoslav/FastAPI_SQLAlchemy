from typing import Union

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from components.post.models import Post


class PostService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: dict, user_id: int) -> Post:
        post = Post(**data, user_id=user_id)
        self._session.add(post)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def get_post_by_id(self, post_id: int) -> Union[Post, None]:
        query = select(Post).where(Post.id == post_id).options(selectinload(Post.comments))
        try:
            post = (await self._session.exec(query)).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Post does not exists.")

        return post

    async def delete(self, post_id: int) -> None:
        post = await self._session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post does not exists.")

        await self._session.delete(post)
        await self._session.commit()
