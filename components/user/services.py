from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from components.user.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: dict) -> User:
        user = User(**data)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        user = await self._session.execute(query)
        return user.scalar()

    async def get_user_by_id(self, user_id: str) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        user = await self._session.execute(query)
        return user.scalar()
