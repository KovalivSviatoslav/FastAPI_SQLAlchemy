from sqlalchemy.ext.asyncio import AsyncSession

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
