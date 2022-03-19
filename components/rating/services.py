from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from components.rating.models import Rating


class RatingService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: dict, user_id: int) -> Rating:
        rating = Rating(**data, user_id=user_id)
        self._session.add(rating)
        await self._session.commit()
        await self._session.refresh(rating)
        return rating

    async def update(self, comment_id: int, data: dict) -> Rating:
        rating = await self._session.get(Rating, comment_id)
        if not rating:
            raise HTTPException(status_code=404, detail="Rating does not exists.")

        for key, value in data.items():
            setattr(rating, key, value)

        self._session.add(rating)
        await self._session.commit()
        await self._session.refresh(rating)
        return rating
