from typing import Union, List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from components.post.models import Post
from components.rating.models import Rating


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

    async def get_posts(self) -> List[Post]:
        query = select(Post)
        posts = (await self._session.exec(query)).all()
        return posts

    async def update(self, post_id: int, data: dict) -> Post:
        post = await self._session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post does not exists.")

        for key, value in data.items():
            setattr(post, key, value)

        self._session.add(post)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def get_avg_rating(self):
        await self._session.execute(
            update(Post).values(
                avg_rating=select(
                    func.round(func.avg(Rating.value), 0)
                ).where(Rating.post_id == Post.id).scalar_subquery()
            )
        )
        await self._session.commit()
