from typing import Union, List, Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from components.post.elastic import PostIndexService
from components.post.models import Post, Category
from components.rating.models import Rating


class PostService:
    def __init__(self, session: AsyncSession, es_service: Optional[PostIndexService] = None):
        self._session = session
        self._es_service = es_service

    async def create(self, data: dict, user_id: int) -> Post:
        category = await CategoryService(self._session).get_or_create(data.pop('category'))
        post = Post(**data, user_id=user_id, category=category)
        self._session.add(post)
        await self._session.flush()
        await self._session.refresh(post)
        post.category = category

        await self._es_service.put_doc(post)
        await self._session.commit()
        return post

    async def get_post_by_id(self, post_id: int) -> Union[Post, None]:
        query = select(Post).where(Post.id == post_id).options(
            selectinload(Post.comments),
            selectinload(Post.category)
        )
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
        await self._session.flush()

        await self._es_service.delete_doc(post)
        await self._session.commit()

    async def get_posts(self) -> List[Post]:
        query = select(Post)
        posts = (await self._session.exec(query)).all()
        return posts

    async def update(self, post_id: int, data: dict) -> Post:
        post = await self._session.get(Post, post_id)
        category = await CategoryService(self._session).get_or_create(data['category'])
        data["category"] = category
        if not post:
            raise HTTPException(status_code=404, detail="Post does not exists.")

        for key, value in data.items():
            setattr(post, key, value)

        self._session.add(post)
        await self._session.flush()
        await self._session.refresh(post)

        await self._es_service.update_doc(post)
        await self._session.commit()
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


class CategoryService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_or_create(self, name: str) -> Category:
        query = select(Category).where(Category.name == name)
        try:
            category = (await self._session.exec(query)).one()
        except NoResultFound:
            category = Category(name=name)
            self._session.add(category)
            await self._session.commit()
            await self._session.refresh(category)

        return category
